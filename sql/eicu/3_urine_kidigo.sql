-- we have joined each row to all rows preceding within 24 hours  
-- we can now sum these rows to get total UO over the last 24 hours  
-- we can use case statements to restrict it to only the last 6/12 hours  
-- therefore we have three sums:  
-- 1) over a 6 hour period  
-- 2) over a 12 hour period  
-- 3) over a 24 hour period  
-- note that we assume data charted at chartoffset corresponds to 1 hour of UO  
-- therefore we use '5' and '11' to restrict the period, rather than 6/12  
-- this assumption may overestimate UO rate when documentation is done less than hourly  
-- 6 hours  
-- DROP MATERIALIZED VIEW IF EXISTS kdigo_uo CASCADE;
-- CREATE MATERIALIZED VIEW kdigo_uo AS 
with ur_stg as (
    select io.patientunitstayid,
        io.chartoffset,
        sum(
            case
                when make_interval(mins =>io.chartoffset) <= make_interval(mins => iosum.chartoffset) + INTERVAL '5 HOURS' then iosum.urineoutput
                else null
            end
        ) as UrineOutput_6hr,
        sum(
            case
                when make_interval(mins =>io.chartoffset) <= make_interval(mins => iosum.chartoffset) + INTERVAL '11 HOURS' then iosum.urineoutput
                else null
            end
        ) as UrineOutput_12hr,
        sum(iosum.urineoutput) as UrineOutput_24hr,
        ROUND(
            CAST(
                EXTRACT(
                    EPOCH
                    FROM make_interval(mins =>io.chartoffset) - MIN(
                            case
                                when make_interval(mins =>io.chartoffset) <= make_interval(mins => iosum.chartoffset) + INTERVAL '5 HOURS' then make_interval(mins =>iosum.chartoffset)
                                else null
                            end
                        )
                ) / 3600.0 AS NUMERIC
            ),
            4
        ) AS uo_tm_6hr,
        ROUND(
            CAST(
                EXTRACT(
                    EPOCH
                    FROM make_interval(mins =>io.chartoffset) - MIN(
                            case
                                when make_interval(mins =>io.chartoffset) <= make_interval(mins => iosum.chartoffset) + INTERVAL '11 HOURS' then make_interval(mins =>iosum.chartoffset)
                                else null
                            end
                        )
                ) / 3600.0 AS NUMERIC
            ),
            4
        ) AS uo_tm_12hr,
        ROUND(
            CAST(
                EXTRACT(
                    EPOCH
                    FROM make_interval(mins =>io.chartoffset) - make_interval(mins =>MIN(iosum.chartoffset))
                ) / 3600.0 AS NUMERIC
            ),
            4
        ) AS uo_tm_24hr
    from urineoutput io
        left join urineoutput iosum on io.patientunitstayid = iosum.patientunitstayid
        and io.chartoffset >= iosum.chartoffset
        and make_interval(mins => io.chartoffset) <= (
            make_interval(mins => iosum.chartoffset) + INTERVAL '23 HOURS'
        )
    group by io.patientunitstayid,
        io.chartoffset
)
select ur.patientunitstayid,
    ur.chartoffset,
    wd.weight,
    ur.UrineOutput_6hr,
    ur.UrineOutput_12hr,
    ur.UrineOutput_24hr,
    ROUND(
        (ur.UrineOutput_6hr / wd.weight /(uo_tm_6hr + 1))::NUMERIC,
        4
    ) AS uo_rt_6hr,
    ROUND(
        (
            ur.UrineOutput_12hr / wd.weight /(uo_tm_12hr + 1)
        )::NUMERIC,
        4
    ) AS uo_rt_12hr,
    ROUND(
        (
            ur.UrineOutput_24hr / wd.weight /(uo_tm_24hr + 1)
        )::NUMERIC,
        4
    ) AS uo_rt_24hr,
    uo_tm_6hr,
    uo_tm_12hr,
    uo_tm_24hr
from ur_stg ur -- 
    left join weightdurations wd on ur.patientunitstayid = wd.patientunitstayid
    and ur.chartoffset >= wd.starttime -- 
    and ur.chartoffset < wd.endtime
order by patientunitstayid,
    chartoffset;