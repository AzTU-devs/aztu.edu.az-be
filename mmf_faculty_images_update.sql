-- MMF (Maşınqayırma Mühəndisliyi Fakültəsi) profile_image updates
-- Image base path: /media/prod/faculty/machine_faculty/

-- Dean
UPDATE faculty_directors
SET profile_image = '/media/prod/faculty/machine_faculty/Malik Qarayev.JPG',
    updated_at = NOW()
WHERE id = 17 AND faculty_code = 'MMF';

-- Deputy Deans
UPDATE faculty_deputy_deans
SET profile_image = '/media/prod/faculty/machine_faculty/elgun_sebiyev.jpg',
    updated_at = NOW()
WHERE id = 19 AND faculty_code = 'MMF';

UPDATE faculty_deputy_deans
SET profile_image = '/media/prod/faculty/machine_faculty/Anar Hacıyev.JPG',
    updated_at = NOW()
WHERE id = 20 AND faculty_code = 'MMF';

-- Workers
UPDATE faculty_workers
SET profile_image = '/media/prod/faculty/machine_faculty/Göyçək Qaloyeva-Rzayeva.JPG',
    updated_at = NOW()
WHERE id = 44 AND faculty_code = 'MMF';

UPDATE faculty_workers
SET profile_image = '/media/prod/faculty/machine_faculty/Fatimə Zülfüqarova.JPG',
    updated_at = NOW()
WHERE id = 45 AND faculty_code = 'MMF';

UPDATE faculty_workers
SET profile_image = '/media/prod/faculty/machine_faculty/Gülnarə Babayeva.JPG',
    updated_at = NOW()
WHERE id = 46 AND faculty_code = 'MMF';

UPDATE faculty_workers
SET profile_image = '/media/prod/faculty/machine_faculty/Nazilə Nəbiyeva.JPG',
    updated_at = NOW()
WHERE id = 47 AND faculty_code = 'MMF';

UPDATE faculty_workers
SET profile_image = '/media/prod/faculty/machine_faculty/Ülkər Cabbarlı.jpeg',
    updated_at = NOW()
WHERE id = 48 AND faculty_code = 'MMF';
