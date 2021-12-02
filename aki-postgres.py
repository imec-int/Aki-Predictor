import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import dotenv
from sqlalchemy import create_engine
from pathlib import Path
import argparse


def test_postgres(cursor):
    cursor.execute("""
SELECT
    *
FROM
   pg_catalog.pg_tables
WHERE
   schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
    """)

    tables = cursor.fetchall()

    print("List of tables:")
    for table in tables:
        print(table)

    # construct an engine connection string
    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASWORD", "postgres"),
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", 5432),
        database=os.getenv("DATABASE_NAME", "mimic"),
        sslmode=os.getenv("DATABASE_SSL_MODE", 'disable'),

    )

    if os.getenv("DATABASE_SSL_MODE", 'disable') == 'require':
        engine_string = engine_string + " ?sslmode=require"

    # create sqlalchemy engine
    engine = create_engine(engine_string)

    # read a table from database into pandas dataframe
    for table in tables:
        tn = table[1]
        print("Table {}".format(tn))

        df = pd.read_sql_table(tn, engine)

        print("Head of extracted pandas DF:")
        print(df.head())


def execute_sql(cursor, path):
    for i in sorted(os.listdir(path)):
        print("accessing file: "+i)
        sql_file = open(os.path.join(path, i), 'r')
        cursor.execute(sql_file.read())
        print("view "+str(i)+" created")


def save_sql(conn, sql_path, save_path):
    # TODO not tested yet
    for i in sorted(os.listdir(sql_path)):
      # we split on the dot, the second part is the name of the file to save, the first part is the order of execution, last is extension
        filename = i.split(".")[1]
        print("accessing save file: "+filename)
        sql_file = open(os.path.join(sql_path, i), 'r')
        # cursor.execute(sql_file.read())
        df = pd.read_sql_query(sql_file.read(), conn)
        # df.to_csv(os.path.join(save_path, filename+".csv"),
        #           encoding='utf-8', header=True)
        df.to_parquet(path=os.path.join(save_path, filename+".parquet"))


def run(dbname):
    print(dbname)
    # MIMIC
    if(dbname == 'mimiciii'):
        print("we're accessing the MIMIC-III dB")
        try:
            conn = psycopg2.connect(
                host=os.getenv("DATABASE_HOST_MIMIC"),
                user=os.getenv("DATABASE_USER_MIMIC"),
                password=os.getenv("DATABASE_PASSWORD_MIMIC"),
                database=os.getenv("DATABASE_NAME_MIMIC"),
                sslmode=os.getenv("DATABASE_SSL_MODE"),
                options=f'-c search_path=mimiciii,public'
            )
            cursor = conn.cursor()
        except Exception as error:
            print(error)
    else:
        # eICU
        print("we're accessing the eICU dB")
        try:
            conn = psycopg2.connect(
                host=os.getenv("DATABASE_HOST_EICU"),
                user=os.getenv("DATABASE_USER_EICU"),
                password=os.getenv("DATABASE_PASSWORD_EICU"),
                database=os.getenv("DATABASE_NAME_EICU"),
                sslmode=os.getenv("DATABASE_SSL_MODE"),
                options=f'-c search_path=eicu_crd,public'
            )
            cursor = conn.cursor()
        except Exception as error:
            print(error)

    # test_postgres(cursor)

    execute_sql(cursor, path=Path.cwd() / 'sql' / dbname)
    save_sql(conn, sql_path=Path.cwd() / 'sql' / 'save',
             save_path=Path.cwd() / 'output' / dbname)


if __name__ == '__main__':
    dbname_constant = 'eicu' # in case of no python arguments

    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", type=str, help="choose database name: eicu or mimiciii", choices=[
                        'eicu', 'mimiciii'])
    args = parser.parse_args()

    run(dbname=args.dbname) if args.dbname else run(dbname=dbname_constant)
