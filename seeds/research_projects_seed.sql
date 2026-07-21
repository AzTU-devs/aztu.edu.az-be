-- =====================================================================
-- SEED — Research Projects (Tədqiqat Layihələri)
--
-- OPTIONAL. Run `migrations_research_projects.sql` first.
--
-- Loads the four projects supplied by the university. Idempotent: rows are
-- keyed by a fixed project_code, so re-running updates in place rather than
-- duplicating.
--
-- ⚠️  The Azerbaijani copy is verbatim from the source document. The English
--     rows carry translated *metadata* only (name, type, duration, budget);
--     `about_html` is deliberately left empty because translating these
--     scientific abstracts is an editorial decision, not a migration's job.
--     Fill the English "Haqqında" in the dashboard before relying on /en.
--
--     Project 900003's source link was truncated ("https://www.aef.gov.az/
--     upload/...") so it is left null rather than guessed.
-- =====================================================================

begin;

-- ── Parents ──────────────────────────────────────────────────────────
insert into research_projects (project_code, project_url, created_at, updated_at) values
    ('900001', 'https://www.aef.gov.az/az/grant/view/57',                        now(), now()),
    ('900002', 'http://www.mgs.gost.ru/TKSUGGEST/MGSpublic.nsf/MainForm?ReadForm', now(), now()),
    ('900003', null,                                                             now(), now()),
    ('900004', null,                                                             now(), now())
on conflict (project_code) do update
    set project_url = excluded.project_url,
        updated_at  = now();


-- ── Azerbaijani translations ─────────────────────────────────────────
insert into research_projects_tr
    (project_code, lang_code, name, project_type, duration, leader_name, budget, about_html, created_at, updated_at)
values
(
    '900001', 'az',
    'Azad Fəzada Optik Rabitəli Maneəyə Davamlı Nanopeyk Modelinin İşlənilməsi və Tədqiqi',
    'Elmi tədqiqat',
    'iki il',
    'Həsənov Mehman Hüseyn oğlu',
    '800000',
    $html$<p>Layihənin məqsədi azad fəzada optik rabitəni özündə birləşdirən model yaratmaqla nanopeykin rabitə effektivliyini artırmaqdır. Nanopeyklər optik rabitə vasitəsilə informasiyanın daha sürətli və təhlükəsiz şəkildə ötürülməsinə imkan verir. Bu layihədə azad fəzada optik rabitənin iş prinsipləri, həmçinin texnoloji və təbii amillərin (məsələn, atmosfer maneələri) rabitəyə təsiri araşdırılacaq. Layihənin qarşıya qoyulan məsələləri aşağıdakılardır: nanopeyk modelinin dizaynı və inkişafı, optik rabitə sisteminin hazırlanması, təsir amillərinin tədqiqi, optik rabitənin səmərəliliyinin yoxlanılması və enerji effektivliyi ilə peykin avtonom fəaliyyətinin təmin olunması.</p><p>Nanopeyk texnologiyası üçün lazım olan kompakt və səmərəli dizaynın hazırlanması, peykin quraşdırılması və kosmik mühitdə uğurlu əməliyyatın təmin edilməsi üçün lazımi sistemlərin inteqrasiyası həyata keçiriləcək. Azad fəzada optik rabitə məqsədilə tələb olunan texnologiyaların kosmos şərtlərinə uyğunluğu araşdırılacaq, atmosfer şəraitinin, kosmik radiasiyanın, müdaxilələrin və digər xarici amillərin rabitə keyfiyyətinə və peyk performansına təsiri öyrəniləcək, bu təsirləri azaltmaq üçün həll yolları müəyyən ediləcək. Optik rabitə siqnallarının bütövlüyü, ötürmə qabiliyyəti və ünsiyyət sürəti yoxlanılacaq, atmosfer şəraitində işığın yayılma xüsusiyyətlərini araşdırmaq üçün eksperimental təcrübələr və simulyasiyalar aparılacaq. Eyni zamanda peyklərin uzunmüddətli fəaliyyətini təmin edəcək və enerji sərfiyyatını azaldacaq enerji mənbələri və idarəetmə sistemləri yaradılacaq.</p><p>Layihənin aktuallığı ondan ibarətdir ki, CubeSat tipli nanopeyklər artan sürətlə genişlənən kosmik rabitə sistemləri sahəsində əsaslı texnoloji irəliləyişləri asanlaşdırır. Bu sistemlər üçün optik rabitə geniş bant genişliyi ilə təhlükəsiz, yüksək sürətli məlumat ötürülməsini təmin edir. Adi radiorabitədən fərqli olaraq, optik rabitə daha yüksək məlumat ötürmə qabiliyyəti və azaldılmış müdaxilə riski təklif edir. Gələcək peyk təşəbbüslərinin inkişafına atmosferin və kosmik şəraitin rabitə vasitələrinə təsirinin tədqiqi kömək edəcək. Layihə elmi tədqiqatlar sahəsində son dərəcə aktualdır və müasir telekommunikasiya və kosmik texnologiyalar üçün vacib olan innovasiyaların həyata keçirilməsini vurğulayır.</p><p>Bu layihə kosmik texnologiyalar, optik fizika, rabitə texnologiyaları, mühəndislik və telekommunikasiya texnologiyaları kimi müxtəlif elmi və texnoloji sahələri birləşdirən multidissiplinar bir yanaşmaya malikdir. Layihə nanopeyk texnologiyalarına aid olan CubeSat modeli əsasında optik rabitə sistemlərinin qurulmasını və bu sistemlərin azad fəza mühitində nə qədər effektiv olduğunu tədqiq etməyi hədəfləyir. Layihənin əsas məqsədi azad fəzada optik rabitə texnologiyaları ilə təchiz edilmiş CubeSat nanopeykinin modelinin hazırlanması və işlənməsi, azad fəzada yüksək sürətli məlumat ötürmə qabiliyyətinin təmin edilməsi və bu sistemə təsir edən kənar amillərin (məsələn, atmosfer, istilik və mexaniki gərginliklərin optik siqnallara təsiri) araşdırılmasıdır. Layihənin elmi əsası kiçik ölçülü peyklərdə (məsələn, CubeSat) yüksək sürətli məlumat ötürülməsi məqsədilə elektromaqnit spektrini genişləndirmək və ənənəvi radio rabitədən daha effektiv və səmərəli olan optik rabitənin asan şəkildə istifadəsini təmin etməkdən ibarətdir. Layihə həmçinin orbital dinamika, atmosfer təsirləri, istilik və mexaniki yüklərin peykin rabitə sisteminə təsirini tədqiq edəcək. Gözlənilən nəticələrə optik rabitə sistemləri ilə inteqrasiya olunmuş yüksək performanslı CubeSat tipli modellərinin yaradılması, onların qiymətləndirilməsi və azad fəzada informasiya ötürülməsinin səmərəliliyinin artırılması daxildir. Optik rabitənin istifadəsi vasitəsilə CubeSat tipli nanopeyklərin daha geniş elmi və texniki məqsədlər üçün istifadəsi hədəflənir. Layihənin nəticələri əsasında kiçik peyk sistemlərinin səmərəliliyini və uzunömürlülüyünü artırmaq, gələcəkdə onların genişmiqyaslı tətbiqlərini asanlıqla həyata keçirmək gözlənilir. Layihənin praktiki əhəmiyyəti isə yüksək performanslı, lakin daha aşağı maliyyətli nanopeyk sistemlərinin hazırlanmasından, bununla yanaşı elmi tədqiqatlar, müşahidə, məlumat toplama və digər kosmik əməliyyat sahələrində istifadənin mümkünlüyünü təmin etməkdən ibarətdir.</p><p>Optik rabitə texnologiyası peyk rabitə sistemlərində nisbətən yeni olsa da, onun tətbiqi ilə bağlı intensiv tədqiqatlar aparılır. Optik rabitə radiotezliyə əsaslanan rabitə sistemləri ilə müqayisədə daha yüksək bant genişliyinə, daha sürətli məlumat ötürmə imkanlarına və elektromaqnit müdaxiləsinə qarşı daha yüksək toxunulmazlığa malikdir. Buna baxmayaraq, azad fəzada optik rabitə texnologiyalarının istifadəsi müxtəlif texnoloji maneələr yaradır. Bu texnologiyanın geniş tətbiqinə əsas maneə olaraq atmosfer şəraitinin, dispersiya və atmosfer zəifləmə faktorlarının optik siqnalın keyfiyyətinə təsirini göstərmək olar. Bu sahədə müxtəlif ölkələrdə aparılan elmi tədqiqatlar göstərir ki, nanopeyklər üçün optik rabitənin tətbiqi həm nəzəri, həm də praktiki çərçivədə inkişaf etdirilməlidir. Məsələn, NASA və ESA çoxsaylı optik rabitə təşəbbüsləri həyata keçirib. NASA-nın Laser Communications Relay Demonstration (LCRD) proqramı kosmosun tədqiqi məqsədilə lazer əsaslı rabitə sistemlərinin qiymətləndirilməsini həyata keçirir. Bu proqram RF rabitə sistemlərini əvəz etmək üçün lazer texnologiyasının potensialını nümayiş etdirən qabaqcıl tədqiqat layihələrindən biridir. Bundan əlavə, Avropa Kosmik Agentliyi (ESA) “Avropa Data Relay System” (EDRS) vasitəsilə məlumatların ötürülməsi üçün lazer rabitəsi sahəsində əsaslı tədqiqatlar aparmışdır. Starlink peyklər arasında lazer əsaslı optik rabitə texnologiyasını tətbiq etməklə sürətli və fasiləsiz məlumat ötürülməsini təmin edir, bu da internet xidmətində gecikməni azaldır. Bu texnologiya CubeSat-lar kimi nanopeyklərin gələcəkdə daha effektiv və genişmiqyaslı rabitə şəbəkələrində istifadə edilməsi üçün yeni imkanlar yaradır. Layihə müəlliflərinin elmi istiqaməti üzrə elmi-təcrübi nailiyyətləri də bu istiqamətdə böyük əhəmiyyət daşıyır. Son 5 il ərzində layihənin rəhbəri Mehman Həsənov və həm-rəhbər Əli Tağıyev layihənin elmi istiqaməti üzrə geniş araşdırmalar aparmış, mövzu ilə bağlı çoxsaylı elmi məqalələr dərc etdirmişlər. Layihənin icraçılarının da bu mövzu barəsində araşdırmaları, patentləri və ixtiraları mövcuddur. Elmi-təcrübi araşdırmalardan biri süni neyron analizindən istifadə edərək azad fəzada optik şəbəkələrin adaptiv monitorinqinə həsr olunmuşdur. Digər mühüm nəticə isə lazer şüasının ötürülməsindən istifadə edən nanopeykin konseptual modelinin işlənməsi və onun bərpa olunan elektrik enerjisinin yığılmasında əhəmiyyətinin müəyyən edilməsidir. Layihə rəhbərləri tərəfindən nanopeyklərdən ötürülən siqnalları optimal qəbul etmək üçün antenaların üzərində quraşdırılan piezomotor texnologiyası üzrə də geniş tədqiqatlar aparılmış və bəzi qurğular üçün patentlər əldə edilmişdir. Bununla belə, layihənin əsas tədqiqat hədəfi olan sahə üzrə hələ də çoxlu həll olunmamış məsələlər qalmaqdadır. Atmosfer təsirlərinin optik rabitəyə təsirinin tam aradan qaldırılması problemi hələ müasir texnologiyalarla tam həll edilməmişdir. Peyklərdəki optik rabitə sistemlərinin minimal enerjisi yüksək keyfiyyətli siqnalların uzaq məsafələrə ötürülməsində müəyyən çətinliklər yaradır. Əlavə olaraq Azərbaycanda milli CubeSat-in olmaması ölkənin kosmik texnologiyalar sahəsində xarici asılılığını artırır və yerli elmi-texnoloji inkişafı məhdudlaşdırır. Milli CubeSat platformasının yaradılması müstəqil kosmik infrastruktur qurmağa, elm və texnologiya sahəsində yeni biliklər əldə etməyə və strateji təhlükəsizliyi təmin etməyə imkan verəcək. Bu layihə həm də yerli mütəxəssislərin hazırlanmasına və ölkənin regionda kosmik sahədə mövqeyinin güclənməsinə töhfə verəcək. Göstərilən problemlərin həlli üçün yeni qurğular, lazer texnologiyaları və daha mürəkkəb siqnal emal üsulları üzərində davamlı tədqiqatlar aparılmalıdır. Layihə müəlliflərinin elmi təcrübəsi və bilikləri bu sahədə üstün nəticələr əldə etmək üçün istifadə ediləcək.</p>$html$,
    now(), now()
),
(
    '900002', 'az',
    '200 MPa-a qədər geniş temperatur və təzyiq diapazonunda 1-butanolun istilik-fiziki xüsusiyyətlərinin öyrənilməsinə',
    'Elmi-tədqiqat',
    '2022-2025',
    'prof. Həsənov V.H.',
    'yox',
    $html$<p>Bu layihənin əsas məqsədi 1-butanolun geniş temperatur və yüksək təzyiq (200 MPa-a qədər) diapazonlarında istilik-fiziki xüsusiyyətlərini dəqiq müəyyənləşdirmək və bu məlumatlar əsasında onun texnoloji proseslərdə tətbiq imkanlarını qiymətləndirməkdir.</p><p>Layihənin əsas əhəmiyyəti və aktuallığı ondan ibarətdir ki, 1-butanol alternativ yanacaq və sənaye həlledicisi kimi perspektivli maddədir. Onun yüksək temperatur və təzyiq şəraitində davranışının öyrənilməsi enerji, kimya və neft-kimya sənayesində mühüm tətbiqlərə yol aça bilər. İqlim dəyişikliyi və enerji keçidi dövründə bu tip tədqiqatlar böyük əhəmiyyət kəsb edir.</p><p>Layihədə 1-butanolun istilik-fiziki parametrlərinin təyin olunması üçün eksperimental şəraitin qurulmuş, müxtəlif təzyiq və temperatur rejimlərində ölçmələrin aparılmış və alınan nəticələrin analizi və mövcud ədəbiyyatla müqayisəsi aparılmışdır. Layihə eksperimental və hesablama üsullarının birləşdirilməsi ilə həyata keçiriləcək. Laborator şəraitdə yüksək dəqiqlikli cihazlardan istifadə olunacaq, daha sonra nəticələr müvafiq termodinamik modellərlə təhlil ediləcəkdir.</p><p>Layihənin əsas istiqaməti geniş diapazonda 1-butanol üçün dəqiq istilik-fiziki xassələrin cədvəl və qrafiklərlə təqdim olunması, mövcud modellərin uyğunluğunun qiymətləndirilməsi və təkmilləşdirilməsi üçün yeni təkliflər, tətbiq sahələri üçün elmi əsaslandırılmış tövsiyələr.</p><p>Layihənin nəticələri enerji mühəndisliyi, istilik mübadiləsi sistemləri, bioyanacaq texnologiyaları və kimya sənayesində tətbiq oluna bilər. Eyni zamanda alınmış məlumatlar simulyasiya proqramlarında istifadə edilərək real proseslərin daha dəqiq modelləşdirilməsinə töhfə verəcək. Bu da texnoloji proseslərin səmərəliliyinin artırılması və enerji itkilərinin azaldılması ilə nəticələnməsi nəzərdə tutulub.</p>$html$,
    now(), now()
),
(
    '900003', 'az',
    '“Əsas qrant müsabiqəsi-2023” (AEF-MCG-2023-1(43))',
    'Azərbaycan Elm Fondu',
    '01 dekabr 2023-cü il – 01 dekabr 2025-ci il',
    'Məmmədov Arif Tapdıq oğlu',
    '250 min manat',
    $html$<p><strong>Layihənin adı:</strong> yerli resurslar əsasında legirli poladlar və ferroərintilər istehsalı texnologiyalarının işlənməsi.</p><p>Layihənin məqsədi yerli xammaldan istifadə etməklə ferroərintilərin istehsal proseslərinin işlənməsi və ölkənin metallurgiya müəssisələrində legirli poladlarının istehsalının təşkilindən ibarətdir.</p><p>Layihənin elmi ideyasını ilk dəfə ferroərintilər istehsalında yerli xammalın istifadəsi əsasında mürəkkəb fiziki-kimyəvi və metallurji proseslərin, termodinamiki parametrlərin aşkarlanması, poladın oksigensizləşdirilməsi və legirlənməsində ferroərintilərin rolunun qiymətləndirilməsi təşkil edir. Bu postulat əsasında alınan legirli poladlarının istehsal rejimləri, struktur və xassələri arasında qarşılıqlı əlaqənin qurulması da tədqiqatların elmi ideyasını təşkil edir.</p><p>Layihənin gözlənilən elmi nəticələri yerli xammal əsasında işlənmiş legirli polad və ferroərintilərin poladın oksigensizləşdirmə prosesinin keyfiyyətin yüksəldilməsinə, nəticədə daha keyfiyyətli elektrik poladının alınmasını təmin edir. Məhz poladın keyfiyyətinin artırılması onun müxtəlif konstruksiyalar üçün istifadəsinə imkan verəcəkdir.</p><p>Tədqiqatlar nəticəsində alınmış elmi nəticələr metallurgiya və materialşünaslıq sahəsində innovativ yanaşmalar əsasında yeni müddəaların formalaşmasına imkan verə bilər. İşlənmiş müddəalar metallurgiya istehsalında və müvafiq ixtisasların tədris proqramlarında istifadə oluna bilər.</p><p>Layihənin elmi istiqaməti yerli xammaldan istifadə etməklə ferroərintilərin istehsalının təşkili üçün tədqiqatların aparılmasıdır. Ferroərintilər əsasən polad və çuqunun istehsalında istifadə olunur. Ferroərintilərin keyfiyyəti metallurgiya məhsullarının keyfiyyətinə birbaşa təsir edir.</p><p>Legirli poladlar istehsalı üçün ferroərintilərin (ferroxrom, ferrotitan, ferrobor və s.) olması isə keyfiyyətli poladların alınmasına mane olur. Ona görə də ölkəyə legirli poladlar xarici ölkələrdən idxal olunur.</p><p>Azərbaycanda ferroərintilər istehsalı üçün yerli xammaldan istifadə olunmur. Bu, həm metal məmulların keyfiyyətinə mənfi təsir edir, istehsalın ritmini pozur və onun maya dəyərini yüksəldir. Ona görə də xarici ölkələrdə, o cümlədən Rusiya, Ukrayna, İran və Türkiyədə istehsal olunan ferroərintilər baha başa gəlir, həm də yüksək keyfiyyətli polad istehsalının təşkilinə imkan vermir. Ölkəmizdə istehsal olunan ferroərintilər xarici xammal əsasında alınır.</p><p>Ona görə də layihədə təqdim olunan yaradıcı kollektiv legirli poladlar və ferroərintilər üçün yerli xammalın axtarışını aparmışdır. Ferrosilisium istehsalı üçün kvars qumu mədənləri aşkar edilmiş və kvars qumları tədqiq olunmuşdur. Alınmış nəticələr müsbətdir və yüksək keyfiyyətli ferrosilisium istehsal etməyə imkan verə bilər.</p><p><strong>Layihənin elmi ideyası:</strong> Yerli xammal əsasında alınmış ferroərintilərin polad istehsalında istifadə olunması, texnoloji proseslərin termodinamiki parametrləri və kimyəvi sintez reaksiyalarının tarazlıq əmsallarının təyin edilməsi layihənin əsas elmi hipotezini təşkil edir. Uyğun metalların ferroərintilərinin alınması üçün metal oksidlərindən istifadə etməklə elə bərpaedicilər seçilməlidir ki, bərpa şəraitində faydalı elementi təkrar emal olunan xammaldan çıxara bilsin.</p><p>Məhz bu elmi postulat əsasında yerli xammaldan ferroərintilərin istehsal texnologiyasının işlənməsi nəzərdə tutulur. Bu texnologiya ferroərintilər üçün xammalın selektiv seçimi əsasında işlənəcəkdir. Bu halda yaradıcı kollektiv ferroərintilərin alınmasının üç əsas metodunu tədqiq etməyi planlaşdırır: karbonotermik, silikotermik və alüminotermik reduksiya.</p><p>Göstərilən elmi ideya əsasında ferroərintilərin istehsalı yüksəkkeyfiyyətli xüsusi xassəli poladların ölkədə istehsalına imkan verəcəkdir.</p><p><strong>Layihədən gözlənilən əməli nəticələr:</strong></p><ol><li>Ferroərintilərin istehsalı üçün yerli xammalın selektiv seçimlə həyata keçirilməsi polad istehsalında yeni metodun işlənməsini labüd edəcəkdir.</li><li>Silikotermiki və alüminotermiki üsullarla ferroərintilər istehsalının təşkili azkarbonlu ferroərintilərin alınması konsepsiyasının əsasını təşkil edəcəkdir.</li><li>Ferroərintilər istehsalı üçün elektroqövs sobasının istifadə olunması enerjiyə və resurslara qənaətli texnologiyaların nəzəri və praktiki əsaslarının işlənməsinə imkan verəcəkdir.</li><li>Yüksək keyfiyyətli ferroərintilərin tətbiqi elektropolad istehsalında yeni yanaşmanı ortaya çıxaracaq və bu yanaşma əsasında keyfiyyətli poladların ölkədə istehsalına stimul verəcəkdir.</li></ol><p><strong>Tətbiq sahələri:</strong> Layihə çərçivəsində aparılmış tədqiqatların nəticələri metallurgiya və maşınqayırma müəssisələri, gəmiqayırma və gəmi təmiri, elektrotexnika və energetika, neft-qaz və kimya sənayesi, habelə kənd təsərrüfatında istifadə oluna bilər.</p><p>Metallurgiya texnologiyaları sahəsində texniki və texnoloji işləmələr polad və çuqunların keyfiyyətinin yüksəldilməsinə, maşınqayırmada yeni qurğuların hazırlanmasında daha keyfiyyətli metal məmulların tətbiqinə, gəmiqayırmada ölkə daxilində istehsal olunan poladların istifadəsinə, kənd təsərrüfatında metal əsaslı müxtəlif gübrələrin istehsalına imkan verəcəkdir.</p>$html$,
    now(), now()
),
(
    '900004', 'az',
    'Süni intellekt metodlarından istifadə edərək funksional keçidli yeni növ kompozit materialların dayanıqlıq problemlərinin modelləşdirilməsi',
    'Yeni elmi prinsiplərin, nəzəri modellərin və metodların işlənməsi məqsədi daşıyır. Əldə olunan nəzəri biliklərin praktik problemlərin həllinə yönəldilməsi və nəticədə real texnoloji və mühəndislik nəticələri əldə etmək. Elmi nəticələrin bazar yönümlü məhsula çevrilməsi (patent, istehsal, texnologiya transferi).',
    '1 il (12 ay)',
    'Piriyev Sahib Aydın oğlu',
    '30000 manat (otuz min manat)',
    $html$<p>Layihənin məqsədi süni intellekt metodları və riyazi modelləşdirmə yanaşmaları əsasında funksional keçidli (FGM) yeni nəsil kompozit materialların dayanıqlıq və deformasiya davranışının proqnozlaşdırılması üçün nəzəri və hesablama modellərinin işlənməsidir.</p><p>Bu məqsədlə layihədə aşağıdakı əsas istiqamətlər həyata keçiriləcək:</p><ol><li>FGM kompozit materialların elastiklik və möhkəmlik xassələrinin dəyişkən struktur funksiyaları əsasında modelləşdirilməsi;</li><li>Süni intellekt alqoritmlərinin (neyron şəbəkə, genetik alqoritm və s.) tətbiqi ilə material parametrləri və zədələnmə meyarlarının identifikasiyası;</li><li>Dayanıqlıq, gərginlik və zədələnmə proqnozlarının AI modelləri ilə klassik mexanika nəticələri ilə müqayisəli analizi;</li><li>Əldə olunan nəticələr əsasında yeni optimallaşdırılmış kompozit material növlərinin təklif edilməsi.</li></ol><p>Müasir mühəndislikdə və materialşünaslıqda funksional keçidli materiallar (Functionally Graded Materials, FGM) və kompozit strukturlar ən perspektivli istiqamətlərdən biridir. Bu materiallar müxtəlif fiziki və mexaniki xassələri (möhkəmlik, sərtlik, istilikkeçirmə, elastiklik və s.) tədricən dəyişən formada daşıdıqları üçün kəskin gərginlik sıçrayışlarını azaldır, çat əmələ gəlməsini ləngidir və istismar müddətini artırır. Eyni zamanda, süni intellekt (AI) metodları — xüsusilə neyron şəbəkələr, genetik alqoritmlər və qeyri-səlis məntiq modelləri — materialların davranışının proqnozlaşdırılmasında və zədələnmə mexanizmlərinin analitik modelləşdirilməsində yeni imkanlar açır. Bu yanaşmalar eksperimental tədqiqatlara olan ehtiyacı azaldır, hesablama xərclərini minimuma endirir və daha çevik optimallaşdırma sistemləri qurmağa imkan verir.</p><p>Bu layihənin aktuallığı ondan ibarətdir ki, burada ənənəvi elastiklik nəzəriyyəsi ilə süni intellekt yanaşması birləşdirilərək, FGM kompozitlərin dayanıqlıq və zədələnmə modelləri hazırlanacaq. Belə bir yanaşma həm elmi yenilik, həm də tətbiqi mühəndislik baxımından əhəmiyyətlidir. Layihənin nəticələri aerokosmik, avtomobil və enerji sənayesində tətbiq oluna biləcək yeni nəsil ağıllı materialların layihələndirilməsinə töhfə verəcək.</p><p><strong>Metodologiya:</strong> FGM materialların mexaniki davranışını təsvir edən əsas diferensial tənliklər tərtib ediləcək; bu tənliklər materialın qeyri-bircinsliyini, yəni elastiklik modulunun və ya sıxlığın radial və ya istiqamət üzrə dəyişməsini nəzərə alacaq. Materiallarda yaddaş effekti və zamanla dəyişən xassələrin modelləşdirilməsi üçün zamandan asılı olaraq qeyri-xətti operatorlar tətbiq ediləcək. Alınmış tənliklərin analitik həlli çətin olduqda ədədi həll üsullarından — Runge-Kutta üsulu, sonlu elementlər üsulu (FEM) və s. — istifadə olunacaq.</p><p>Süni intellekt yanaşmaları: neyron şəbəkələr — model parametrlərini təxmin və optimallaşdırmaq üçün; genetik alqoritmlər — optimal material tərkibini müəyyənləşdirmək üçün; qeyri-səlis məntiq — qeyri-müəyyənlik şəraitində qərarvermə üçün. MATLAB, Python və ANSYS kimi proqram təminatları vasitəsilə modellərin simulyasiyası aparılacaq və nəticələr analitik və ya ədəbiyyatdakı məlumatlarla müqayisə edilərək yoxlanılacaq.</p><p><strong>Gözlənilən nəticələr:</strong></p><ul><li>Yeni nəzəri model: FGM kompozitlərin gərginlik-deformasiya vəziyyətini və dayanıqlıq limitlərini təsvir edən yeni riyazi model və ya fraksional tənliklər sistemi;</li><li>AI əsaslı proqnozlaşdırma alqoritmi: zədələnmə və elastiklik proqnozlaşdırma modulu;</li><li>Optimallaşdırılmış material strukturu: dayanıqlığı və enerji udma qabiliyyəti yüksək olan funksional keçidli kompozit material tərkibləri;</li><li>Ədədi simulyasiya nəticələri: gərginlik paylanması, deformasiyanın dinamik inkişafı və zədələnmə zonalarının yayılması qrafik və sayısal formada;</li><li>Scopus və WoS indeksli jurnallarda elmi məqalələr və konfrans tezisləri;</li><li>Milli elmi potensiala töhfə: yerli tədqiqatlarda süni intellekt metodlarının tətbiqinin genişləndirilməsi;</li><li>Tətbiqi əhəmiyyət: ağıllı kompozit materialların istehsalında, aerokosmik və müdafiə sənayesində, eləcə də mühəndislik konstruksiyalarında istifadə.</li></ul><p><strong>Nəticələrin tətbiqi və təsiri:</strong> Layihə nəticələri həm elmi-nəzəri, həm də praktiki-tətbiqi baxımdan mühüm əhəmiyyət daşıyır. Elmi təsir: FGM materialların dayanıqlıq problemlərinin süni intellekt metodları ilə modelləşdirilməsi sahəsində orijinal yanaşma təklif olunacaq; materialşünaslıq, tətbiqi mexanika və hesablama metodları sahəsində yerli elmi məktəbin güclənməsinə töhfə veriləcək; nəticələr beynəlxalq jurnal və konfranslarda yayımlanaraq Azərbaycanın elmi nüfuzunu artıracaq. Tətbiqi təsir: mexaniki yüklənmələrə qarşı optimal müqavimət göstərən FGM kompozitlərin tərkibi və struktur dizaynı müəyyən ediləcək; nəticələr müdafiə, aerokosmik, avtomobil və tikinti sənayesində tətbiq oluna biləcək; MATLAB/Python əsaslı sayısal modelləşdirmə proqram modulu gələcək layihələr üçün baza kimi xidmət edəcək. İqtisadi və sosial təsir: yerli istehsalda innovativ, yüngül və möhkəm kompozit materialların hazırlanması imkanlarını artıracaq; gənc tədqiqatçıların və doktorantların iştirakını təmin etməklə elmi kadr potensialının formalaşmasına dəstək verəcək.</p>$html$,
    now(), now()
)
on conflict (project_code, lang_code) do update
    set name         = excluded.name,
        project_type = excluded.project_type,
        duration     = excluded.duration,
        leader_name  = excluded.leader_name,
        budget       = excluded.budget,
        about_html   = excluded.about_html,
        updated_at   = now();


-- ── English translations (metadata only — see the warning at the top) ─
insert into research_projects_tr
    (project_code, lang_code, name, project_type, duration, leader_name, budget, about_html, created_at, updated_at)
values
    ('900001', 'en',
     'Development and Research of an Interference-Resistant Nanosatellite Model with Free-Space Optical Communication',
     'Scientific research', 'two years', 'Mehman Huseyn Hasanov', '800000', '', now(), now()),
    ('900002', 'en',
     'Study of the Thermophysical Properties of 1-Butanol over a Wide Temperature and Pressure Range up to 200 MPa',
     'Scientific research', '2022-2025', 'Prof. V.H. Hasanov', '—', '', now(), now()),
    ('900003', 'en',
     '“Main Grant Competition-2023” (AEF-MCG-2023-1(43))',
     'Azerbaijan Science Foundation', '01 December 2023 – 01 December 2025',
     'Arif Tapdig Mammadov', '250 thousand manat', '', now(), now()),
    ('900004', 'en',
     'Modelling the Stability Problems of a New Type of Functionally Graded Composite Materials Using Artificial Intelligence Methods',
     'Development of new scientific principles, theoretical models and methods',
     '1 year (12 months)', 'Sahib Aydin Piriyev', '30000 manat (thirty thousand manat)', '', now(), now())
on conflict (project_code, lang_code) do update
    set name         = excluded.name,
        project_type = excluded.project_type,
        duration     = excluded.duration,
        leader_name  = excluded.leader_name,
        budget       = excluded.budget,
        updated_at   = now();


-- ── Team members ─────────────────────────────────────────────────────
-- Replaced wholesale so re-running the seed cannot duplicate the roster.
delete from research_project_members where project_code in ('900001', '900002', '900003', '900004');

insert into research_project_members (project_code, full_name, display_order, created_at, updated_at) values
    ('900001', 'Tağıyev Əli Daşdəmir oğlu',      0, now(), now()),
    ('900001', 'Piriyev Sahib Aydin oğlu',       1, now(), now()),
    ('900001', 'Nəcəfov Baloğlan Kamil oğlu',    2, now(), now()),
    ('900001', 'Camalzadə Nuranə İqbal qızı',    3, now(), now()),
    -- 900002 has no team members listed in the source document.
    ('900003', 'Babayev A.İ.',                   0, now(), now()),
    ('900003', 'Namazov S.N.',                   1, now(), now()),
    ('900003', 'Hüseynov M.Ç.',                  2, now(), now()),
    ('900003', 'Quliyev F.T.',                   3, now(), now()),
    ('900003', 'İsmayılov N.Ş.',                 4, now(), now()),
    ('900003', 'Bayramov A.T.',                  5, now(), now()),
    ('900003', 'Babayev H.İ.',                   6, now(), now()),
    ('900003', 'Musurzayeva B.B.',               7, now(), now()),
    ('900004', 'Rüstəmova Məhsəti Akif qızı',    0, now(), now()),
    ('900004', 'Məmmədova Güldəstə Akif qızı',   1, now(), now()),
    ('900004', 'Əzimov Fizuli Murad oğlu',       2, now(), now());

commit;


-- ── Verify ───────────────────────────────────────────────────────────
select p.project_code,
       max(tr.name) filter (where tr.lang_code = 'az') as name_az,
       count(distinct tr.lang_code)                    as languages,
       (select count(*) from research_project_members m
         where m.project_code = p.project_code)         as members
from research_projects p
left join research_projects_tr tr on tr.project_code = p.project_code
where p.project_code in ('900001', '900002', '900003', '900004')
group by p.project_code
order by p.project_code;
