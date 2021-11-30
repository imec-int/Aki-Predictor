import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import dotenv
from sqlalchemy import create_engine
from pathlib import Path


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


# def urine_output(cursor,dbname):
#     sql_file = open(os.path.join('sql', dbname, ''), 'r')
#     cursor.execute(sql_file.read())

# def creatinine(cursor,dbname):
#     sql_file = open(os.path.join('sql', dbname, '4_creatinine.sql'), 'r')
#     cursor.execute(sql_file.read())


# def weight_duration(cursor,dbname):
#     # -- This query extracts weights for ICU patients with start/stop times
#     # -- if only an admission weight is given, then this is assigned from intime to outtime
#     sql_file = open(os.path.join('sql', dbname, '2_weight_duration.sql'), 'r')
#     cursor.execute(sql_file.read())

# def urine_kidigo(cursor,dbname):
#     #      -- we have joined each row to all rows preceding within 24 hours \
#     #               -- we can now sum these rows to get total UO over the last 24 hours \
#     #               -- we can use case statements to restrict it to only the last 6/12 hours \
#     #               -- therefore we have three sums: \
#     #               -- 1) over a 6 hour period \
#     #               -- 2) over a 12 hour period \
#     #               -- 3) over a 24 hour period \
#     #               -- note that we assume data charted at charttime corresponds to 1 hour of UO \
#     #               -- therefore we use '5' and '11' to restrict the period, rather than 6/12 \
#     #               -- this assumption may overestimate UO rate when documentation is done less than hourly \
#     #               -- 6 hours \
#     sql_file = open(os.path.join('sql', dbname, '3_urine_kidigo.sql'), 'r')
#     cursor.execute(sql_file.read())


# def kidigo_7_days_creatinine(cursor,dbname):
#     # -- This query checks if the patient had AKI during the first 7 days of their ICU
#     # -- stay according to the KDIGO guideline.
#     # -- https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf
#     sql_file = open(os.path.join('sql', dbname, '8_kidigo_7_days_creatinine.sql'), 'r')
#     cursor.execute(sql_file.read())


# def kidigo_stages_creatinine(cursor,dbname):
#     # -- This query checks if the patient had AKI according to KDIGO.
#     # -- AKI is calculated every time a creatinine or urine output measurement occurs.
#     # -- Baseline creatinine is defined as the lowest creatinine in the past 7 days.
#     sql_file = open(os.path.join('sql', dbname, '8_kidigo_7_days_creatinine.sql'), 'r')
#     cursor.execute(sql_file.read())


# def kidigo_7_days(cursor,dbname):
#     # -- This query checks if the patient had AKI during the first 7 days of their ICU
#     # -- stay according to the KDIGO guideline.
#     # -- https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf
#     sql_file = open(os.path.join('sql', dbname, '6_kidigo_7_days.sql'), 'r')
#     cursor.execute(sql_file.read())


# def kidigo_stages(cursor,dbname):
#     # -- This query checks if the patient had AKI according to KDIGO.
#     # -- AKI is calculated every time a creatinine or urine output measurement occurs.
#     # -- Baseline creatinine is defined as the lowest creatinine in the past 7 days.
#     sql_file = open(os.path.join('sql', dbname, '5_kidigo_stages.sql'), 'r')
#     cursor.execute(sql_file.read())


# def get_labevents(cursor,dbname):
#     # -- This query pivots lab values taken during the 7 first days of  a patient's stay
#     # -- Have already confirmed that the unit of measurement is always the same: null or the correct unit

#     # -- Extract all bicarbonate, blood urea nitrogen (BUN), calcium, chloride, creatinine,
#     # hemoglobin, international normalized ratio (INR), platelet, potassium, prothrombin time (PT),
#     # partial throm- boplastin time (PTT), and white blood count (WBC) values from labevents around patient's ICU stay
#     sql_file = open(os.path.join('sql', dbname, '9_get_labevents.sql'), 'r')
#     cursor.execute(sql_file.read())

# def save_labevents(conn, dbname):
#     sql_file = open(os.path.join('sql', dbname, '10_labstay.sql'), 'r')
#     df = pd.read_sql_query(sql_file, conn)
#     df.to_csv(os.path.join('csv', dbname, "labstay.csv"), encoding='utf-8', header=True)

# def get_vitals_chart(cursor,dbname):
#     # -- This query pivots the vital signs during the first 7 days of a patient's stay
#     # -- Vital signs include heart rate, blood pressure, respiration rate, and temperature
#     sql_file = open(os.path.join('sql', dbname, '11_get_vitals.sql'), 'r')
#     cursor.execute(sql_file.read())

# def save_vitals(conn, dbname):
#     sql_file = open(os.path.join('sql', dbname, '12_vitalsfirstday.sql'), 'r')
#     df = pd.read_sql_query(sql_file, conn)
#     df.to_csv(os.path.join('csv', dbname, "chart_vitals_stay.csv"), encoding='utf-8', header=True)

# def get_comorbidities(cursor,dbname):
#     sql_file = open(os.path.join('sql', dbname, '13_get_comorbidities.sql'), 'r')
#     cursor.execute(sql_file.read())
# def save_comorbidities(conn, dbname):
#     sql_file = open(os.path.join('sql', dbname, '14_sel_comorbidities.sql'), 'r')
#     df = pd.read_sql_query(sql_file, conn)
#     df.to_csv(os.path.join('csv', dbname, "comorbidities.csv"), encoding='utf-8', header=True)

# def count_icustays(cursor,dbname):
#     sql_file = open(os.path.join('sql', dbname, '15_count_icustays.sql'), 'r')
#     cursor.execute(sql_file.read())

def execute_sql(path):
    for i in sorted(os.listdir(path)):
        print("accessing file: "+i)
        sql_file = open(os.path.join(path, i), 'r')
        cursor.execute(sql_file.read())
        print("view "+str(i)+"created")


def save_sql(sql_path, save_path):
    # TODO not tested yet
    for i in sorted(os.listdir(sql_path)):
      # we split on the dot, the second part is the name of the file to save, the first part is the order of execution, last is extension
        filename = i.split(".")[1]
        print("accessing save file: "+filename)
        sql_file = open(os.path.join(sql_path, i), 'r')
        df = pd.read_sql_query(sql_file, conn)
        df.to_csv(os.path.join(save_path, filename+".csv"),
                  encoding='utf-8', header=True)


if __name__ == '__main__':
    dbname = 'mimiciii'  # 'eicu'

    load_dotenv()
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
                options=f'-c search_path=mimiciii'
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
                options=f'-c search_path=eicu_crd'
            )
            cursor = conn.cursor()

        except Exception as error:
            print(error)

    # test_postgres(cursor)

    execute_sql(path=Path.cwd() / 'sql' / dbname)
    save_sql(sql_path=Path.cwd() / 'save',
             save_path=Path.cwd() / 'output' / dbname)

    # urine_output(cursor, dbname)
    # print("view urine_output created")

    # weight_duration(cursor, dbname)
    # print("view weight_duration created")

    # urine_kidigo(cursor,dbname)
    # print("view urine_kidigo created")

    # creatinine(cursor,dbname)
    # print("view creatinine created")

    # kidigo_stages(cursor,dbname)
    # print("view kidigo_stages created")
    # query = "select * from kdigo_stages"
    # df = pd.read_sql_query(query, conn)
    # df.to_csv(os.path.join('csv', dbname, "AKI_KIDIGO_STAGES_SQL.csv"), encoding='utf-8', header=True)

    # kidigo_7_days(cursor,dbname)
    # print("view kidigo_7_days created")
    # query = "select * from kdigo_stages_7day"
    # df = pd.read_sql_query(query, conn)
    # df.to_csv(os.path.join('csv', dbname, "AKI_KIDIGO_7D_SQL.csv"), encoding='utf-8', header=True)

    # kidigo_stages_creatinine(cursor,dbname)
    # print("view kidigo_stages_creatinine created")
    # query = "select * from kdigo_stages_creatinine"
    # df = pd.read_sql_query(query, conn)
    # df.to_csv(os.path.join('csv', dbname, "AKI_KIDIGO_STAGES_SQL_CREATININE.csv"), encoding='utf-8', header=True)

    # kidigo_7_days_creatinine(cursor,dbname)
    # print("view kidigo_7_days_creatinine created")
    # query = "select * from kdigo_7_days_creatinine"
    # df = pd.read_sql_query(query, conn)
    # df.to_csv(os.path.join('csv', dbname, "AKI_KIDIGO_7D_SQL_CREATININE.csv"), encoding='utf-8', header=True)

    # get_labevents(cursor,dbname)

    # save_labevents(conn, dbname)

    # get_vitals_chart(cursor,dbname)

    # save_vitals(conn, dbname)

    # get_comorbidities(cursor,dbname)

    # save_comorbidities(conn, dbname)

    # count_icustays(cursor,dbname)
