import os
from dateutil.parser import parse
import shutil


def is_date(string, fuzzy=False):
	"""
	Return whether the string can be interpreted as a date.

	:param string: str, string to check for date
	:param fuzzy: bool, ignore unknown tokens in string if True
	"""
	try:
		parse(string, fuzzy=fuzzy)
		return True

	except ValueError:
		return False


# Init
notebook_folder = '/home/willw/pop-os/home/willwalker/OneDrive/Notebooks/Notes/'
project_wiki_folder = notebook_folder + 'Projects_Wiki'
resume_wiki_folder = notebook_folder + 'Resumes_Wiki'

project_folder = '/home/willw/pop-os/home/willwalker/OneDrive/Projects'
resume_folder = '/home/willw/pop-os/home/willwalker/OneDrive/Resumes'

# Checking what is in the wiki and what is in the folders
projects = next(os.walk(project_folder))[1]
projects_added = next(os.walk(project_wiki_folder))[1]
for project in projects:
	if project not in projects_added:
		# open file to write to
		with open(project_wiki_folder + '/' + project + '.txt', 'w+') as d:
			# open source file from project folder
			with open(project_folder + '/' + project + '/README.md', 'r') as s:
				# Write README to wiki
				d.write(s.read())

# Checking what is in the wiki and what is in the folders
resumes = next(os.walk(resume_folder))[1]
resumes_added = next(os.walk(resume_wiki_folder))[1]
for folders, subfolders, filenames in os.walk(resume_folder):
	for filename in filenames:
		if filename.endswith('.pdf'):
			shutil.copy(os.path.join(folders, filename), resume_wiki_folder)
