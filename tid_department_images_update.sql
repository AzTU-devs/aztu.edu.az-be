-- TID (Tədqiqat və İnkişaf Departamenti / research_dev_department) profile_image updates
-- Image base path: /media/prod/departments/tid/

-- Director: Bəxtiyar Bədəlov
UPDATE department_directors
SET profile_image = '/media/prod/departments/tid/bakhtiyar_badalov.png',
    updated_at = NOW()
WHERE department_code = 'research_dev_department'
  AND first_name = 'Bəxtiyar' AND last_name = 'Bədəlov';

-- Workers
UPDATE department_workers
SET profile_image = '/media/prod/departments/tid/kemale_tehmezova.jpg',
    updated_at = NOW()
WHERE department_code = 'research_dev_department'
  AND email = 'tehmezova.kemale@aztu.edu.az';

UPDATE department_workers
SET profile_image = '/media/prod/departments/tid/natavan_babayeva.jpg',
    updated_at = NOW()
WHERE department_code = 'research_dev_department'
  AND email = 'natavan.babayeva@aztu.edu.az';

UPDATE department_workers
SET profile_image = '/media/prod/departments/tid/fatma_tagiyeva.jpg',
    updated_at = NOW()
WHERE department_code = 'research_dev_department'
  AND email = 'fatma.tagiyeva@aztu.edu.az';

UPDATE department_workers
SET profile_image = '/media/prod/departments/tid/nargiz_ismayilova.jpg',
    updated_at = NOW()
WHERE department_code = 'research_dev_department'
  AND email = 'nargiz.ismayilova@aztu.edu.az';
