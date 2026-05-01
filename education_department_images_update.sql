-- Education Department (Tədris şöbəsi) profile_image updates
-- Image base path: /media/prod/departments/education/

-- Director: Ərəstun Məmmədov (id=4)
UPDATE department_directors
SET profile_image = '/media/prod/departments/education/mammadiov_arastun.jpg',
    updated_at = NOW()
WHERE id = 4 AND department_code = 'education_department';

-- Staff
UPDATE department_workers
SET profile_image = '/media/prod/departments/education/jafarova_elnura.jpg',
    updated_at = NOW()
WHERE id = 10 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Allazova Ulviyya.jpg',
    updated_at = NOW()
WHERE id = 11 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Abdurahimova Jamila.jpg',
    updated_at = NOW()
WHERE id = 12 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Mirzayeva Sevinj.jpg',
    updated_at = NOW()
WHERE id = 13 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Allahverdiyeva Sakina.jpg',
    updated_at = NOW()
WHERE id = 14 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Aliyev Kamil.jpg',
    updated_at = NOW()
WHERE id = 15 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Karimova Gunay.jpg',
    updated_at = NOW()
WHERE id = 16 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Musayeva Parvana.jpg',
    updated_at = NOW()
WHERE id = 17 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Israfilov Yashar.jpg',
    updated_at = NOW()
WHERE id = 18 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Rzayev Ramin.jpg',
    updated_at = NOW()
WHERE id = 19 AND department_code = 'education_department';

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Jabarova Aida.jpg',
    updated_at = NOW()
WHERE id = 20 AND department_code = 'education_department';

-- id=21 Tahirə Təhməzova: no image provided
-- id=22 Xəyalə Quliyeva: no image provided

UPDATE department_workers
SET profile_image = '/media/prod/departments/education/Aslanova Aychillar.jpg',
    updated_at = NOW()
WHERE id = 23 AND department_code = 'education_department';
