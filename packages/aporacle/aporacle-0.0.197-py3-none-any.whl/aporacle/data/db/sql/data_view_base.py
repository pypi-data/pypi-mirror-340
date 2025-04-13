import logging
import os
from typing import Optional, Dict, List

from komoutils.core import KomoBase
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseConfigurationError(Exception):
    """Exception raised when there are issues with database configuration."""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


class DataViewBase(KomoBase):
    def __init__(self):
        """
        Initialize the DataViewBase with empty configuration.
        Inheriting classes should set the database configuration.
        """
        super().__init__()
        self.db_name = None
        self.db_user = None
        self.db_password = None
        self.db_host = None
        self.db_port = None
        self.db_url = None
        self.async_db_url = None
        self.engine = None
        self.session = None
        self.async_engine = None
        self.async_session = None

    def setup_connection(self):
        """
        Set up the database connections based on the configuration.
        This method should be called after setting the configuration properties.
        
        Raises:
            DatabaseConfigurationError: If any required configuration is missing
        """
        errors = self._validate_configuration()
        if errors:
            raise DatabaseConfigurationError(errors)
            
        # Create the fully formed db_urls for SQLAlchemy
        self.db_url = f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.async_db_url = f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

        # Create sync engine and session (default)
        self.engine = create_engine(self.db_url)
        self.session = sessionmaker(bind=self.engine)

        # Create async engine and session (optional)
        self.async_engine = create_async_engine(self.async_db_url)
        self.async_session = sessionmaker(bind=self.async_engine, class_=AsyncSession)

    def _validate_configuration(self) -> List[str]:
        """
        Validate that all required configuration fields are set.
        
        Returns:
            List[str]: List of error messages, empty if configuration is valid
        """
        errors = []
        required_fields = {
            'db_name': self.db_name,
            'db_user': self.db_user,
            'db_password': self.db_password,
            'db_host': self.db_host,
            'db_port': self.db_port
        }
        
        for field, value in required_fields.items():
            if value is None or value == '':
                errors.append(f"Missing required configuration field: {field}")
                
        return errors

    def check_database_and_credentials(self):
        """
        Verify database configuration and credentials.
        Collects all errors and raises them together.
        
        Returns:
            bool: True if all checks pass
            
        Raises:
            DatabaseConfigurationError: If any configuration or connection issues are found
        """
        # First validate configuration
        config_errors = self._validate_configuration()
        if config_errors:
            raise DatabaseConfigurationError(config_errors)
            
        # Ensure engines are set up
        if not self.engine:
            raise DatabaseConfigurationError(["Database engines not initialized. Call setup_connection() first."])
            
        errors = []
        
        try:
            with self.engine.connect() as connection:
                # Check if the database exists
                result = connection.execute(text(f"SHOW DATABASES LIKE '{self.db_name}'"))
                if not result.fetchone():
                    errors.append(f"Database '{self.db_name}' does not exist.")
                    
                # Try to use the database if it exists
                try:
                    connection.execute(text(f"USE {self.db_name}"))
                    connection.execute(text("SELECT 1"))
                except SQLAlchemyError as e:
                    errors.append(f"Cannot access database with provided credentials: {str(e)}")
        except SQLAlchemyError as e:
            errors.append(f"Error connecting to database server: {str(e)}")
            
        if errors:
            raise DatabaseConfigurationError(errors)
            
        self.log_with_clock(log_level=logging.INFO, msg="Database configuration and credentials verified successfully.")
        return True

    def check_db_connection(self):
        """
        Test the synchronous database connection.
        
        Returns:
            bool: True if connection is successful
            
        Raises:
            DatabaseConfigurationError: If connection fails
        """
        # Ensure session is set up
        if not self.session:
            raise DatabaseConfigurationError(["Database session not initialized. Call setup_connection() first."])
            
        try:
            with self.session() as session:
                session.execute(text("SELECT 1"))
            self.log_with_clock(log_level=logging.INFO, msg="Database connection successful.")
            return True
        except SQLAlchemyError as e:
            raise DatabaseConfigurationError([f"Error connecting to the database: {str(e)}"])

    async def check_async_db_connection(self):
        """
        Test the asynchronous database connection.
        
        Returns:
            bool: True if connection is successful
            
        Raises:
            DatabaseConfigurationError: If connection fails
        """
        # Ensure async session is set up
        if not self.async_session:
            raise DatabaseConfigurationError(["Async database session not initialized. Call setup_connection() first."])
            
        try:
            async with self.async_session() as session:
                await session.execute(text("SELECT 1"))
            self.log_with_clock(log_level=logging.INFO, msg="Async database connection successful.")
            return True
        except SQLAlchemyError as e:
            raise DatabaseConfigurationError([f"Error connecting to the async database: {str(e)}"])

