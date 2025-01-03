-- query_analytics_voter_details
SELECT
    vd.MobileNumber AS voter_id, 
    vd.VoterName AS name,
    vd.Constituency AS region,
    vd.Gender,
    vd.MaritalStatus,
    vd.EducationQualification AS education_level,
    vd.Schemes AS associated_schemes,
    now() AS job_created_date,
    'admin' AS job_created_user
FROM stage.voter_details vd
INNER JOIN analytics.dim_constituency_region dcr ON dcr.constituency_name = vd.Constituency
WHERE NOT EXISTS (
    SELECT 1 
    FROM analytics.dim_voter av 
    WHERE av.voter_id = vd.MobileNumber
);