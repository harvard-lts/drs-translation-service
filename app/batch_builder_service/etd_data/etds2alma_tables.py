# flake8: noqa
# Look-up tables used by our etds2alma_pq.py script to map values found 
# in the batch's mets file to what is used in the marcxml sent to Alma

# A Python dictionary (or associtive array or hash)
# to map degree name to what's used in datafield 502 subfield a
degreeCodeName = {
	'D.B.A.': 'Doctor of Business Administration',
	'DBA': 'Doctor of Business Administration',
	'Th.D.': 'Doctor of Theology',
	'M Arch': 'Master in Architecture',
	'MDE': 'Master in Design Engineering',
	'MDes': 'Master in Design Studies',
	'MLA': 'Master in Landscape Architecture',
	'MUP': 'Master in Urban Planning',
	'MAUD': 'Master of Architecture in Urban Design',
	'MLAUD': 'Master of Landscape Architecture in Urban Design',
	'DDes': 'Doctor of Design',
	'MMSCI': 'Master of Medical Sciences in Clinical Investigation',
	'MMSc-GHD': 'Master of Medical Sciences in Global Health Delivery',
	'MMSc IMM': 'Master of Medical Sciences in Immunology',
	'MMSc-Med Ed': 'Master of Medical Sciences in Medical Education',
	'M.D.': 'Doctor of Medicine',
	'MD': 'Doctor of Medicine',
	'D.P.H.': 'Doctor of Public Health',
	'DPH': 'Doctor of Public Health',
	'D.S.': 'Doctor of Science',
	'DS': 'Doctor of Science',
	'A.L.M.': 'Master of Liberal Arts',
	'ALM': 'Master of Liberal Arts',
	'A.B.': 'Bachelor of Arts',
	'AB': 'Bachelor of Arts',
	'S.B.': 'Bachelor of Science',
	'SB': 'Bachelor of Science',
	'Ph.D.': 'Doctor of Philosophy',
	'D.Ed.': 'Doctor of Education',
	'Ed.L.D.': 'Doctor of Education Leadership',
	'D.M.Sc.': 'Doctor of Medical Sciences'
 }
 
# A Python dictionary (or associtive array or hash)
# to map degree level to degree level tracing used in datafield 830 subfield p
degreeLevelTracing = {
	"Bachelor's": "Theses",
	"Undergraduate": "Theses",
	"Masters": "Theses",
	"Doctoral": "Dissertations"
}

# A Python dictionary (or associtive array or hash) of dictionaries
# to translate the school name to the term used in the subfield a and b 
# of the 710 datafield. Also used to set if degree level tracing is used.
schools = {
	'Harvard Business School':
		{'subfield_a': 'Harvard Business School', 'subfield_b': False, 'degree_level_tracing': False, 'lib_code_3_char': 'BAK'},
	'Harvard College':
		{'subfield_a': 'Harvard College (1780- )', 'subfield_b': False, 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard Divinity School':
		{'subfield_a': 'Harvard Divinity School', 'subfield_b': False, 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard Graduate School of Design': 
		{'subfield_a': 'Harvard University' , 'subfield_b': 'Graduate School of Design', 'degree_level_tracing': False, 'lib_code_3_char': 'DES'},
	'Harvard Medical School':
		{'subfield_a': 'Harvard Medical School' , 'subfield_b': False, 'degree_level_tracing': False, 'lib_code_3_char': 'MED'},
	'Harvard T.H. Chan School of Public Health':
		{'subfield_a': 'Harvard T.H. Chan School of Public Health' , 'subfield_b': False, 'degree_level_tracing': False, 'lib_code_3_char': 'MED'},
	'Harvard University Division of Continuing Education':
		{'subfield_a': 'Harvard University' , 'subfield_b': 'Continuing Education Division', 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard University Engineering and Applied Sciences':
		{'subfield_a': 'Harvard College (1780- )' , 'subfield_b': False, 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard University Graduate School of Arts and Sciences':
		{'subfield_a': 'Harvard University' , 'subfield_b': 'Graduate School of Arts and Sciences', 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard University Graduate School of Education':
		{'subfield_a': 'Harvard University' , 'subfield_b': 'Graduate School of Education', 'degree_level_tracing': True, 'lib_code_3_char': 'HUA'},
	'Harvard University School of Dental Medicine':
		{'subfield_a': 'Harvard School of Dental Medicine' , 'subfield_b': False, 'degree_level_tracing': False, 'lib_code_3_char': 'MED'}
}
