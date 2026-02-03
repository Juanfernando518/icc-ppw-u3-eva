-- Datos de prueba para Evaluación Técnica 3
-- Sistema de Gestión de Recursos Humanos

-- Companies
insert into companies (
   id,
   name,
   country,
   active
) values ( 1,
           'TechCorp',
           'USA',
           'S' ),( 2,
                   'InnovateLabs',
                   'Canada',
                   'S' ),( 3,
                           'GlobalSystems',
                           'UK',
                           'N' ),( 4,
                                   'DataMinds',
                                   'Germany',
                                   'S' ),( 5,
                                           'CloudNine',
                                           'Spain',
                                           'S' );

-- Departments
insert into departments (
   id,
   name,
   budget,
   company_id,
   active
) values 
-- TechCorp departments
 ( 1,
           'Engineering',
           250000.00,
           1,
           'S' ),( 2,
                   'Marketing',
                   150000.00,
                   1,
                   'S' ),( 3,
                           'Human Resources',
                           100000.00,
                           1,
                           'S' ),( 4,
                                   'Finance',
                                   180000.00,
                                   1,
                                   'S' ),( 5,
                                           'Sales',
                                           180000.00,
                                           1,
                                           'N' ),

-- InnovateLabs departments
                                           ( 6,
                                                   'Research',
                                                   200000.00,
                                                   2,
                                                   'S' ),( 7,
                                                           'Development',
                                                           220000.00,
                                                           2,
                                                           'S' ),( 8,
                                                                   'Quality Assurance',
                                                                   120000.00,
                                                                   2,
                                                                   'S' ),

-- GlobalSystems departments (empresa inactiva)
                                                                   ( 9,
                                                                           'Operations',
                                                                           150000.00,
                                                                           3,
                                                                           'S' ),

-- DataMinds departments
                                                                           ( 10,
                                                                                   'Data Science',
                                                                                   280000.00,
                                                                                   4,
                                                                                   'S' ),( 11,
                                                                                           'IT Support',
                                                                                           90000.00,
                                                                                           4,
                                                                                           'S' ),

-- CloudNine departments
                                                                                           ( 12,
                                                                                                   'DevOps',
                                                                                                   200000.00,
                                                                                                   5,
                                                                                                   'S' );

-- Employees
insert into employees (
   id,
   first_name,
   last_name,
   email,
   salary,
   department_id,
   active
) values 
-- Engineering (dept 1) - TechCorp
 ( 1,
           'John',
           'Doe',
           'john.doe@techcorp.com',
           5500.00,
           1,
           'S' ),( 2,
                   'Jane',
                   'Smith',
                   'jane.smith@techcorp.com',
                   6200.00,
                   1,
                   'S' ),( 3,
                           'Robert',
                           'Johnson',
                           'robert.johnson@techcorp.com',
                           7500.00,
                           1,
                           'S' ),( 4,
                                   'Michael',
                                   'Brown',
                                   'michael.brown@techcorp.com',
                                   5800.00,
                                   1,
                                   'S' ),( 5,
                                           'Emily',
                                           'Davis',
                                           'emily.davis@techcorp.com',
                                           6500.00,
                                           1,
                                           'S' ),

-- Marketing (dept 2) - TechCorp
                                           ( 6,
                                                   'Sarah',
                                                   'Wilson',
                                                   'sarah.wilson@techcorp.com',
                                                   4800.00,
                                                   2,
                                                   'S' ),( 7,
                                                           'David',
                                                           'Martinez',
                                                           'david.martinez@techcorp.com',
                                                           5200.00,
                                                           2,
                                                           'S' ),( 8,
                                                                   'Laura',
                                                                   'Garcia',
                                                                   'laura.garcia@techcorp.com',
                                                                   4500.00,
                                                                   2,
                                                                   'S' ),

-- Human Resources (dept 3) - TechCorp
                                                                   ( 9,
                                                                           'Jennifer',
                                                                           'Rodriguez',
                                                                           'jennifer.rodriguez@techcorp.com',
                                                                           5000.00,
                                                                           3,
                                                                           'S' ),( 10,
                                                                                   'William',
                                                                                   'Lopez',
                                                                                   'william.lopez@techcorp.com',
                                                                                   5300.00,
                                                                                   3,
                                                                                   'S' ),

-- Finance (dept 4) - TechCorp
                                                                                   ( 11,
                                                                                           'Jessica',
                                                                                           'Hernandez',
                                                                                           'jessica.hernandez@techcorp.com',
                                                                                           6800.00,
                                                                                           4,
                                                                                           'S' ),( 12,
                                                                                                   'Christopher',
                                                                                                   'Moore',
                                                                                                   'christopher.moore@techcorp.com'
                                                                                                   ,
                                                                                                   7200.00,
                                                                                                   4,
                                                                                                   'S' ),( 13,
                                                                                                           'Amanda',
                                                                                                           'Taylor',
                                                                                                           'amanda.taylor@techcorp.com'
                                                                                                           ,
                                                                                                           6000.00,
                                                                                                           4,
                                                                                                           'S' ),

-- Sales (dept 5) - TechCorp - DEPARTAMENTO INACTIVO
                                                                                                           ( 14,
                                                                                                                   'Daniel',
                                                                                                                   'Anderson'
                                                                                                                   ,
                                                                                                                   'daniel.anderson@techcorp.com'
                                                                                                                   ,
                                                                                                                   4700.00,
                                                                                                                   5,
                                                                                                                   'N' ),( 15
                                                                                                                   ,
                                                                                                                        'Matthew'
                                                                                                                        ,
                                                                                                                        'Thomas'
                                                                                                                        ,
                                                                                                                        'matthew.thomas@techcorp.com'
                                                                                                                        ,
                                                                                                                        4900.00
                                                                                                                        ,
                                                                                                                        5,
                                                                                                                        'N' )
                                                                                                                        ,

-- Research (dept 6) - InnovateLabs
                                                                                                                        ( 16,
                                                                                                                            'Lisa'
                                                                                                                            ,
                                                                                                                            'Jackson'
                                                                                                                            ,
                                                                                                                            'lisa.jackson@innovate.com'
                                                                                                                            ,
                                                                                                                            6800.00
                                                                                                                            ,
                                                                                                                            6
                                                                                                                            ,
                                                                                                                            'S'
                                                                                                                            )
                                                                                                                            ,
                                                                                                                            (
                                                                                                                            17
                                                                                                                            ,
                                                                                                                                'Andrew'
                                                                                                                                ,
                                                                                                                                'White'
                                                                                                                                ,
                                                                                                                                'andrew.white@innovate.com'
                                                                                                                                ,
                                                                                                                                7000.00
                                                                                                                                ,
                                                                                                                                6
                                                                                                                                ,
                                                                                                                                'S'
                                                                                                                                )
                                                                                                                                ,
                                                                                                                                (
                                                                                                                                18
                                                                                                                                ,
                                                                                                                                    'Maria'
                                                                                                                                    ,
                                                                                                                                    'Harris'
                                                                                                                                    ,
                                                                                                                                    'maria.harris@innovate.com'
                                                                                                                                    ,
                                                                                                                                    6300.00
                                                                                                                                    ,
                                                                                                                                    6
                                                                                                                                    ,
                                                                                                                                    'S'
                                                                                                                                    )
                                                                                                                                    ,

-- Development (dept 7) - InnovateLabs
                                                                                                                                    
                                                                                                                                    (
                                                                                                                                    19
                                                                                                                                    ,
                                                                                                                                        'Kevin'
                                                                                                                                        ,
                                                                                                                                        'Martin'
                                                                                                                                        ,
                                                                                                                                        'kevin.martin@innovate.com'
                                                                                                                                        ,
                                                                                                                                        5900.00
                                                                                                                                        ,
                                                                                                                                        7
                                                                                                                                        ,
                                                                                                                                        'S'
                                                                                                                                        )
                                                                                                                                        ,
                                                                                                                                        (
                                                                                                                                        20
                                                                                                                                        ,
                                                                                                                                            'Nancy'
                                                                                                                                            ,
                                                                                                                                            'Thompson'
                                                                                                                                            ,
                                                                                                                                            'nancy.thompson@innovate.com'
                                                                                                                                            ,
                                                                                                                                            6100.00
                                                                                                                                            ,
                                                                                                                                            7
                                                                                                                                            ,
                                                                                                                                            'S'
                                                                                                                                            )
                                                                                                                                            ,
                                                                                                                                            (
                                                                                                                                            21
                                                                                                                                            ,
                                                                                                                                                'Steven'
                                                                                                                                                ,
                                                                                                                                                'Lee'
                                                                                                                                                ,
                                                                                                                                                'steven.lee@innovate.com'
                                                                                                                                                ,
                                                                                                                                                5700.00
                                                                                                                                                ,
                                                                                                                                                7
                                                                                                                                                ,
                                                                                                                                                'S'
                                                                                                                                                )
                                                                                                                                                ,
                                                                                                                                                (
                                                                                                                                                22
                                                                                                                                                ,
                                                                                                                                                    'Michelle'
                                                                                                                                                    ,
                                                                                                                                                    'Clark'
                                                                                                                                                    ,
                                                                                                                                                    'michelle.clark@innovate.com'
                                                                                                                                                    ,
                                                                                                                                                    5500.00
                                                                                                                                                    ,
                                                                                                                                                    7
                                                                                                                                                    ,
                                                                                                                                                    'S'
                                                                                                                                                    )
                                                                                                                                                    ,

-- Quality Assurance (dept 8) - InnovateLabs
                                                                                                                                                    
                                                                                                                                                    (
                                                                                                                                                    23
                                                                                                                                                    ,
                                                                                                                                                        'Brian'
                                                                                                                                                        ,
                                                                                                                                                        'Lewis'
                                                                                                                                                        ,
                                                                                                                                                        'brian.lewis@innovate.com'
                                                                                                                                                        ,
                                                                                                                                                        5200.00
                                                                                                                                                        ,
                                                                                                                                                        8
                                                                                                                                                        ,
                                                                                                                                                        'S'
                                                                                                                                                        )
                                                                                                                                                        ,
                                                                                                                                                        (
                                                                                                                                                        24
                                                                                                                                                        ,
                                                                                                                                                            'Rebecca'
                                                                                                                                                            ,
                                                                                                                                                            'Walker'
                                                                                                                                                            ,
                                                                                                                                                            'rebecca.walker@innovate.com'
                                                                                                                                                            ,
                                                                                                                                                            5400.00
                                                                                                                                                            ,
                                                                                                                                                            8
                                                                                                                                                            ,
                                                                                                                                                            'S'
                                                                                                                                                            )
                                                                                                                                                            ,

-- Data Science (dept 10) - DataMinds
                                                                                                                                                            
                                                                                                                                                            (
                                                                                                                                                            25
                                                                                                                                                            ,
                                                                                                                                                                'Thomas'
                                                                                                                                                                ,
                                                                                                                                                                'Hall'
                                                                                                                                                                ,
                                                                                                                                                                'thomas.hall@dataminds.com'
                                                                                                                                                                ,
                                                                                                                                                                8500.00
                                                                                                                                                                ,
                                                                                                                                                                10
                                                                                                                                                                ,
                                                                                                                                                                'S'
                                                                                                                                                                )
                                                                                                                                                                ,
                                                                                                                                                                (
                                                                                                                                                                26
                                                                                                                                                                ,
                                                                                                                                                                    'Patricia'
                                                                                                                                                                    ,
                                                                                                                                                                    'Allen'
                                                                                                                                                                    ,
                                                                                                                                                                    'patricia.allen@dataminds.com'
                                                                                                                                                                    ,
                                                                                                                                                                    8200.00
                                                                                                                                                                    ,
                                                                                                                                                                    10
                                                                                                                                                                    ,
                                                                                                                                                                    'S'
                                                                                                                                                                    )
                                                                                                                                                                    ,
                                                                                                                                                                    (
                                                                                                                                                                    27
                                                                                                                                                                    ,
                                                                                                                                                                        'Charles'
                                                                                                                                                                        ,
                                                                                                                                                                        'Young'
                                                                                                                                                                        ,
                                                                                                                                                                        'charles.young@dataminds.com'
                                                                                                                                                                        ,
                                                                                                                                                                        7800.00
                                                                                                                                                                        ,
                                                                                                                                                                        10
                                                                                                                                                                        ,
                                                                                                                                                                        'S'
                                                                                                                                                                        )
                                                                                                                                                                        ,

-- IT Support (dept 11) - DataMinds
                                                                                                                                                                        
                                                                                                                                                                        (
                                                                                                                                                                        28
                                                                                                                                                                        ,
                                                                                                                                                                            'Barbara'
                                                                                                                                                                            ,
                                                                                                                                                                            'King'
                                                                                                                                                                            ,
                                                                                                                                                                            'barbara.king@dataminds.com'
                                                                                                                                                                            ,
                                                                                                                                                                            4200.00
                                                                                                                                                                            ,
                                                                                                                                                                            11
                                                                                                                                                                            ,
                                                                                                                                                                            'S'
                                                                                                                                                                            )
                                                                                                                                                                            ,
                                                                                                                                                                            (
                                                                                                                                                                            29
                                                                                                                                                                            ,
                                                                                                                                                                                'Joseph'
                                                                                                                                                                                ,
                                                                                                                                                                                'Wright'
                                                                                                                                                                                ,
                                                                                                                                                                                'joseph.wright@dataminds.com'
                                                                                                                                                                                ,
                                                                                                                                                                                4500.00
                                                                                                                                                                                ,
                                                                                                                                                                                11
                                                                                                                                                                                ,
                                                                                                                                                                                'S'
                                                                                                                                                                                )
                                                                                                                                                                                ,

-- DevOps (dept 12) - CloudNine
                                                                                                                                                                                
                                                                                                                                                                                (
                                                                                                                                                                                30
                                                                                                                                                                                ,
                                                                                                                                                                                    'Linda'
                                                                                                                                                                                    ,
                                                                                                                                                                                    'Scott'
                                                                                                                                                                                    ,
                                                                                                                                                                                    'linda.scott@cloudnine.com'
                                                                                                                                                                                    ,
                                                                                                                                                                                    7500.00
                                                                                                                                                                                    ,
                                                                                                                                                                                    12
                                                                                                                                                                                    ,
                                                                                                                                                                                    'S'
                                                                                                                                                                                    )
                                                                                                                                                                                    ,
                                                                                                                                                                                    (
                                                                                                                                                                                    31
                                                                                                                                                                                    ,
                                                                                                                                                                                        'Richard'
                                                                                                                                                                                        ,
                                                                                                                                                                                        'Green'
                                                                                                                                                                                        ,
                                                                                                                                                                                        'richard.green@cloudnine.com'
                                                                                                                                                                                        ,
                                                                                                                                                                                        7300.00
                                                                                                                                                                                        ,
                                                                                                                                                                                        12
                                                                                                                                                                                        ,
                                                                                                                                                                                        'S'
                                                                                                                                                                                        )
                                                                                                                                                                                        ,
                                                                                                                                                                                        (
                                                                                                                                                                                        32
                                                                                                                                                                                        ,
                                                                                                                                                                                            'Susan'
                                                                                                                                                                                            ,
                                                                                                                                                                                            'Adams'
                                                                                                                                                                                            ,
                                                                                                                                                                                            'susan.adams@cloudnine.com'
                                                                                                                                                                                            ,
                                                                                                                                                                                            7100.00
                                                                                                                                                                                            ,
                                                                                                                                                                                            12
                                                                                                                                                                                            ,
                                                                                                                                                                                            'S'
                                                                                                                                                                                            )
                                                                                                                                                                                            ,

-- Algunos empleados inactivos
                                                                                                                                                                                            
                                                                                                                                                                                            (
                                                                                                                                                                                            33
                                                                                                                                                                                            ,
                                                                                                                                                                                                'Mark'
                                                                                                                                                                                                ,
                                                                                                                                                                                                'Baker'
                                                                                                                                                                                                ,
                                                                                                                                                                                                'mark.baker@techcorp.com'
                                                                                                                                                                                                ,
                                                                                                                                                                                                5000.00
                                                                                                                                                                                                ,
                                                                                                                                                                                                1
                                                                                                                                                                                                ,
                                                                                                                                                                                                'N'
                                                                                                                                                                                                )
                                                                                                                                                                                                ,
                                                                                                                                                                                                (
                                                                                                                                                                                                34
                                                                                                                                                                                                ,
                                                                                                                                                                                                    'Carol'
                                                                                                                                                                                                    ,
                                                                                                                                                                                                    'Nelson'
                                                                                                                                                                                                    ,
                                                                                                                                                                                                    'carol.nelson@innovate.com'
                                                                                                                                                                                                    ,
                                                                                                                                                                                                    5500.00
                                                                                                                                                                                                    ,
                                                                                                                                                                                                    7
                                                                                                                                                                                                    ,
                                                                                                                                                                                                    'N'
                                                                                                                                                                                                    )
                                                                                                                                                                                                    ;