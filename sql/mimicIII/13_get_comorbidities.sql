DROP MATERIALIZED VIEW IF EXISTS COMORBIDITIES CASCADE;
CREATE MATERIALIZED VIEW COMORBIDITIES AS with icd as (
    select hadm_id,
        seq_num,
        icd9_code
    from diagnoses_icd
    where seq_num != 1
),
eliflg as (
    select hadm_id,
        seq_num,
        icd9_code,
        CASE
            when icd9_code in (
                '39891',
                '40201',
                '40211',
                '40291',
                '40401',
                '40403',
                '40411',
                '40413',
                '40491',
                '40493'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('4254', '4255', '4257', '4258', '4259') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('428') then 1
            else 0
        end as CHF,
        CASE
            when icd9_code in ('42613', '42610', '42612', '99601', '99604') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '4260',
                '4267',
                '4269',
                '4270',
                '4271',
                '4272',
                '4273',
                '4274',
                '4276',
                '4278',
                '4279',
                '7850',
                'V450',
                'V533'
            ) then 1
            else 0
        end as ARRHY,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('0932', '7463', '7464', '7465', '7466', 'V422', 'V433') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('394', '395', '396', '397', '424') then 1
            else 0
        end as VALVE,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '0930',
                '4373',
                '4431',
                '4432',
                '4438',
                '4439',
                '4471',
                '5571',
                '5579',
                'V434'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('440', '441') then 1
            else 0
        end as PERIVASC,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('401') then 1
            else 0
        end as HTN,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('402', '403', '404', '405') then 1
            else 0
        end as HTNCX,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2500', '2501', '2502', '2503') then 1
            else 0
        end as DM,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2504', '2505', '2506', '2507', '2508', '2509') then 1
            else 0
        end as DMCX,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2409', '2461', '2468') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('243', '244') then 1
            else 0
        end as HYPOTHY,
        CASE
            when icd9_code in (
                '40301',
                '40311',
                '40391',
                '40402',
                '40403',
                '40412',
                '40413',
                '40492',
                '40493'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('5880', 'V420', 'V451') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('585', '586', 'V56') then 1
            else 0
        end as RENLFAIL,
        CASE
            when icd9_code in ('07022', '07023', '07032', '07033', '07044', '07054') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '0706',
                '0709',
                '4560',
                '4561',
                '4562',
                '5722',
                '5723',
                '5724',
                '5728',
                '5733',
                '5734',
                '5738',
                '5739',
                'V427'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('570', '571') then 1
            else 0
        end as LIVER,
        CASE
            when icd9_code in ('72889', '72930') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '7010',
                '7100',
                '7101',
                '7102',
                '7103',
                '7104',
                '7108',
                '7109',
                '7112',
                '7193',
                '7285'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('446', '714', '720', '725') then 1
            else 0
        end as ARTH,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2871', '2873', '2874', '2875') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('286') then 1
            else 0
        end as COAG,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2780') then 1
            else 0
        end as OBESE,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in ('2536') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('276') then 1
            else 0
        end as LYTES,
        CASE
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '2652',
                '2911',
                '2912',
                '2913',
                '2915',
                '2918',
                '2919',
                '3030',
                '3039',
                '3050',
                '3575',
                '4255',
                '5353',
                '5710',
                '5711',
                '5712',
                '5713',
                'V113'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('980') then 1
            else 0
        end as ALCOHOL,
        CASE
            when icd9_code in ('V6542') then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 4
            ) in (
                '3052',
                '3053',
                '3054',
                '3055',
                '3056',
                '3057',
                '3058',
                '3059'
            ) then 1
            when SUBSTRING(
                icd9_code
                FROM 1 for 3
            ) in ('292', '304') then 1
            else 0
        end as DRUG
    from icd
),
eligrp as (
    select hadm_id,
        max(chf) as chf,
        max(arrhy) as arrhy,
        max(valve) as valve,
        max(perivasc) as perivasc,
        max(htn) as htn,
        max(htncx) as htncx,
        max(renlfail) as renlfail,
        max(dm) as dm,
        max(dmcx) as dmcx,
        max(hypothy) as hypothy,
        max(liver) as liver,
        max(arth) as arth,
        max(coag) as coag,
        max(obese) as obese,
        max(lytes) as lytes,
        max(alcohol) as alcohol,
        max(drug) as drug
    from eliflg
    group by hadm_id
)
select adm.hadm_id,
    chf as CONGESTIVE_HEART_FAILURE,
    arrhy as CARDIAC_ARRHYTHMIAS,
    valve as VALVULAR_DISEASE,
    perivasc as PERIPHERAL_VASCULAR,
    renlfail as RENAL_FAILURE,
    case
        when htn = 1 then 1
        when htncx = 1 then 1
        else 0
    end as HYPERTENSION,
    case
        when dmcx = 1 then 0
        when dm = 1 then 1
        else 0
    end as DIABETES_UNCOMPLICATED,
    dmcx as DIABETES_COMPLICATED,
    hypothy as HYPOTHYROIDISM,
    liver as LIVER_DISEASE,
    obese as OBESITY,
    alcohol as ALCOHOL_ABUSE,
    drug as DRUG_ABUSE
from admissions adm
    left join eligrp eli on adm.hadm_id = eli.hadm_id
order by adm.hadm_id;