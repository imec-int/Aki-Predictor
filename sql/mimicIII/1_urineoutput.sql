DROP MATERIALIZED VIEW IF EXISTS urineoutput CASCADE;
CREATE MATERIALIZED VIEW urineoutput as
select oe.icustay_id,
    oe.charttime,
    SUM(
        case
            when oe.itemid = 227488 then -1 * value -- ,,GU Irrigant Volume In,,,227488,GU Irrigant Volume In,mL,outputevents,3157,Output,,,,metavision,,Numeric,
            else value
        end
    ) as value
from outputevents oe
where oe.itemid in (
        40055,
        -- Urine output,Urine output (foley),,verify,,40055,Urine Out Foley,,outputevents,1917527,,,,,carevue,,,
        43175,
        -- Urine output,Urine output,,maybe,,43175,Urine .,,outputevents,108982,,,,,carevue,,,
        40069,
        -- Urine output,Urine output,,verify,,40069,Urine Out Void,,outputevents,69467,,,,,carevue,,,
        40094,
        -- Urine output,Urine output,,verify,,40094,Urine Out Condom Cath,,outputevents,10006,,,,,carevue,,,
        40715,
        -- Urine output,Urine output,,maybe,,40715,Urine Out Suprapubic,,outputevents,6913,,,,,carevue,,,
        40473,
        -- Urine output,Urine output,,maybe,,40473,Urine Out IleoConduit,,outputevents,4813,,,,,carevue,,,
        40085,
        -- ,,,,,40085,Urine Out Incontinent,,outputevents,2891,,,,,carevue,,,
        40057,
        -- ,,,,,40057,Urine Out Rt Nephrostomy,,outputevents,2797,,,,,carevue,,,
        40056,
        -- ,,,,,40056,Urine Out Lt Nephrostomy,,outputevents,2726,,,,,carevue,,,
        40405,
        -- ,,,,,40405,Urine Out Other,,outputevents,1827,,,,,carevue,,,
        40428,
        -- ,,,,,40428,Urine Out Straight Cath,,outputevents,722,,,,,carevue,,,
        40086,
        -- ,,,,,40086,Drain Out #2 Pigtail,,outputevents,1406,,,,,carevue,,,
        40096,
        -- ,,,,,40096,Urine Out Ureteral Stent #1,,outputevents,418,,,,,carevue,,,
        40651,
        -- ,,,,,40651,Urine Out Ureteral Stent #2,,outputevents,90,,,,,carevue,,,
        226559,
        -- Urine output,Urine output (foley),,verify,,226559,Foley,mL,outputevents,1186717,Output,,,,metavision,,Numeric,
        226560,
        -- ,,Void,,,226560,Void,mL,outputevents,63020,Output,,,,metavision,,Numeric,
        226561,
        -- ,,Condom Cath,,,226561,Condom Cath,mL,outputevents,5757,Output,,,,metavision,,Numeric,
        226584,
        -- ,,Ileoconduit,,,226584,Ileoconduit,mL,outputevents,2668,Output,,,,metavision,,Numeric,
        226563,
        -- ,,Suprapubic,,,226563,Suprapubic,mL,outputevents,2499,Output,,,,metavision,,Numeric,
        226564,
        -- ,,R Nephrostomy,,,226564,R Nephrostomy,mL,outputevents,1455,Output,,,,metavision,,Numeric,
        226565,
        -- ,,L Nephrostomy,,,226565,L Nephrostomy,mL,outputevents,1179,Output,,,,metavision,,Numeric,
        226567,
        -- ,,Straight Cath,,,226567,Straight Cath,mL,outputevents,463,Output,,,,metavision,,Numeric,
        226557,
        -- ,,R Ureteral Stent,,,226557,R Ureteral Stent,mL,outputevents,147,Output,,,,metavision,,Numeric,
        226558,
        -- ,,L Ureteral Stent,,,226558,L Ureteral Stent,mL,outputevents,49,Output,,,,metavision,,Numeric,
        227488,
        -- ,,GU Irrigant Volume In,,,227488,GU Irrigant Volume In,mL,outputevents,3157,Output,,,,metavision,,Numeric,
        227489 -- ,,GU Irrigant/Urine Volume Out,,,227489,GU Irrigant/Urine Volume Out,mL,outputevents,3175,Output,,,,metavision,,Numeric,
    )
    and oe.value < 5000
    and oe.icustay_id is not null
group by icustay_id,
    charttime;