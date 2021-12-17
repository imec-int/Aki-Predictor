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
DROP MATERIALIZED VIEW IF EXISTS kdigo_uo CASCADE;
CREATE MATERIALIZED VIEW kdigo_uo AS with ur_stg as (
    select io.patientunitstayid,
        io.chartoffset,
        sum(
            -- we sum for each patientunitstayid over its chartoffset (minutes) and check whether it belongs to output 6hr
            case
                when io.chartoffset <= iosum.chartoffset + 5 * 60 then iosum.urineoutput
                else null
            end
        ) as UrineOutput_6hr,
        sum(
            case
                when io.chartoffset <= iosum.chartoffset + 11 * 60 then iosum.urineoutput
                else null
            end
        ) as UrineOutput_12hr,
        sum(iosum.urineoutput) as UrineOutput_24hr,
        ROUND(
            CAST(
                (
                    io.chartoffset - MIN(
                        case
                            when io.chartoffset <= iosum.chartoffset + 5 * 60 then iosum.chartoffset
                            else null
                        end
                    )
                ) / 60.0 AS NUMERIC
            ),
            4
        ) AS uo_tm_6hr,
        ROUND(
            CAST(
                ( io.chartoffset - MIN(
                    case
                        when io.chartoffset <= iosum.chartoffset + 11 * 60 then iosum.chartoffset
                        else null
                    end
                )
            ) / 60.0 AS NUMERIC
        ),
        4
) AS uo_tm_12hr,
ROUND(
    CAST(
        (io.chartoffset - MIN(iosum.chartoffset)) / 60.0 AS NUMERIC
    ),
    4
) AS uo_tm_24hr
from urineoutput io
    left join urineoutput iosum on io.patientunitstayid = iosum.patientunitstayid
    and io.chartoffset >= iosum.chartoffset
    and io.chartoffset <= iosum.chartoffset + 23 * 60
group by io.patientunitstayid,
    io.chartoffset -- limit 10000
)
select ur.patientunitstayid,
    ur.chartoffset as charttime,
    wd.starttime,
    wd.endtime,
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
    inner join weightdurations wd on ur.patientunitstayid = wd.patientunitstayid --TODO used to be left join, yet we have more urineoutput ids than weight ids...
    and ur.chartoffset >= wd.starttime
    and ur.chartoffset < wd.endtime
    AND uo_tm_6hr is not NULL
    and uo_tm_12hr is not NULL
    and uo_tm_24hr is not NULL
    and wd.weight is not NULL
    and wd.weight not in (0)
order by patientunitstayid,
    charttime;