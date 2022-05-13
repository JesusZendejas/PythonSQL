# Financial planner script
import argparse
import sqlite3
import pandas as pd
import numpy as np
import click
import os

version = '1.0'

def getPathsFromArguments ():
    parser = argparse.ArgumentParser ( description = 'Converts RDBs as defined on SDM40 to new format as defined on SDM41', prog = 'Financial Planner' )
    parser.add_argument ( 'database', metavar='Financial Database', type=str, nargs=1,
                          help='Database with financial information' )
    parser.add_argument ( '--verbosity', '-v', type = int,
                          help='increase output verbosity' )
    parser.add_argument ( '--replace', '-r', action = 'store_const', const = 1,
                          help='Set this if you want SDM40 RDB to be replaced' )
    parser.add_argument ( '--date', '-d', type = str, metavar='Date', help = 'Set the date' )
    parser.add_argument ( '--version', action = 'version', version = '%(prog)s ' + str ( version ) )

    args = parser.parse_args()

    parseRDBs ( args.database[0], args.verbosity, args.replace, args.date )

def parseRDBs ( database, verbosity, replace, date ):

    if ( os.path.exists ( database ) ):
        conn = sqlite3.connect ( database )
        conn.text_factory = lambda b: b.decode ( errors = 'ignore' )
        df = pd.read_sql_query ( "SELECT * from Financial", conn )
        conn.close ()
        df = df.set_index ( [ 'index' ] )

    if ( date ):
        entryDate = date
    else:
        entryDate = '2021-06-10'
    record = pd.Series ({'Date':entryDate,
                         'Expense':'Physics',
                         'Income':85,
                         'FinancialInstrument':' ',
                         'Summary':' ',
                         'Description':' ',
                         'Total':' '} )

    if ( os.path.exists ( database ) ):
        df = df.append ( pd.DataFrame ( [record] ), ignore_index = True )
    else:
        df = pd.DataFrame ( [record] )
        
    day = pd.Timestamp(df.loc[0]['Date'])
        
    df['Date'] = pd.to_datetime ( df.Date )
    df = df.sort_values(by='Date')
    # df.sort ( 'Date' )
    # print ( day.day_name () )
    # print ( df.dtypes )
    print ( df )
    # x = pd.Timestamp ( df ['Date'] )
    # print ( df.loc[0]['Date'] )
    
    if ( replace ):
        if ( replace == 1 ):
            conn   = sqlite3.connect ( database )
            conn.text_factory = lambda b: b.decode ( errors = 'ignore' )
            df.to_sql ( "Financial", conn, if_exists = "replace" )
            conn.close ()
    
def main ( ):
    os.system('cls')
    getPathsFromArguments ()

if __name__ == '__main__':
    main ()
