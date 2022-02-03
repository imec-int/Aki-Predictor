import argparse
import os
import sys

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

from config import config, MIMIC_III, EICU


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


def create_database_connection(cfg):
    if (cfg.dbmodel == MIMIC_III):
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
            return conn
        except Exception as error:
            print(error)
    else: # eICU
        print("we're accessing the eICU dB")
        dbname = cfg.dbname
        if cfg.dbname == "":
            dbname = os.getenv("DATABASE_NAME_EICU")
        try:
            conn = psycopg2.connect(
                host=os.getenv("DATABASE_HOST_EICU"),
                user=os.getenv("DATABASE_USER_EICU"),
                password=os.getenv("DATABASE_PASSWORD_EICU"),
                database=dbname,
                sslmode=os.getenv("DATABASE_SSL_MODE"),
                options=f'-c search_path=eicu_crd,public'
            )
            return conn
        except Exception as error:
            print(error)
            sys.exit(2)


def execute_sql(conn, path):
    for i in sorted(os.listdir(path)):
        cur = conn.cursor()
        try:
            sql_file = open(os.path.join(path, i), 'r')
            print("executing sql file: " + i)
            cur.execute(sql_file.read())
            conn.commit()
        finally:
            cur.close()


def save_sql(conn, sql_path, output_path):
    output_path.mkdir(parents=True, exist_ok=True)
    for i in sorted(os.listdir(sql_path)):
        # we split on the dot, the second part is the name of the file to save, the first part is the order of execution, last is extension
        filename = i.split(".")[1]
        sql_file = open(os.path.join(sql_path, i), 'r')
        df = pd.read_sql_query(sql_file.read(), conn)
        # df.to_csv(os.path.join(save_path, filename+".csv"),
        #           encoding='utf-8', header=True)
        print("saving {} rows to {}: ".format(df.shape[0], filename))
        df.to_parquet(path=os.path.join(output_path, filename + ".parquet"))


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbmodel",
                        type=str,
                        help="choose database model: eicu (default) or mimiciii",
                        choices=['eicu', 'mimiciii']
                        )
    parser.add_argument("--dbname",
                        type=str,
                        help="choose database",
                        )

    cfg = config(parser.parse_args())

    conn = create_database_connection(cfg)

    cursor = conn.cursor()
    execute_sql(conn, cfg.sql_path())

    save_sql(conn,
             sql_path=cfg.save_sql_path(),
             output_path=cfg.queried_path(),
             )
