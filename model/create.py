#! /usr/bin/env python3
# coding: utf-8
"""Class to create database."""

from model.connection import Connection
from model.json import Json

class Create:
    """Create database."""
    def __init__(self, Log, sql_readed):
        self.Log = Log
        # Split the file to make requests list.
        self.SQLrequests = sql_readed.split(';')

    def create_db(self, verbose):
        """Create database (drop if exists)."""
        if verbose:
            print('Erase database if exists.')      
        # Look for database name and erase database if exists.
        DATABASE = Json.read_database_name() 
        self.Log.execute(f"DROP DATABASE IF EXISTS {DATABASE}")   
        self.Log.commit()
        # Count for strings skipped.
        i = 0
        # Execute requests from the list.
        if verbose:
            print('Executing database creation requests.') 
        for request in self.SQLrequests:                   
            try:
                self.Log.execute(request)
            except:
                i+=1
                if verbose:
                    print("String skipped:'",request,"'")                
        # Save information
        self.Log.commit()
        # Disconnect from MySQL Server.
        self.Log.close_connection         
        # Print counter if asked
        if verbose: 
            print(i,'string(s) skipped.')