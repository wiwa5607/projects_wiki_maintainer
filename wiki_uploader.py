from hashlib import new
from re import L
from notion.client import NotionClient
from notion.block import TextBlock
import os
import wiki_maintainer
wiki_maintainer.maintain()
bashCommand = "git config --get remote.origin.url"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

notebook_folder = '/home/willw/pop-os/home/willwalker/OneDrive/Notebooks/Notes/'
project_folder = '/home/willw/pop-os/home/willwalker/OneDrive/Projects'
project_wiki_folder = notebook_folder + 'Projects_Wiki'
project_files = next(os.walk(project_wiki_folder))[2]

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(
	token_v2="da8bcfad6d565ba5bb7f5bb3b6bb61c0515cab67b25f4aa9dab8a3192f2b90eaceed2abd22ed6f65869b73113965116957ae7223413990d46e1da452798b63f6e8050ae900c016d9b366b47dc667")

portfolioCollection = client.get_collection_view(
	"https://www.notion.so/81f77f8d03d741c186e1d3ffc2935bb7?v=e2983b82e4e341eab190ae490477e0f9")

current_entries = [entry.__getattr__(
	'title') for entry in portfolioCollection.collection.get_rows()]

# For every project
for project in project_files:
	project_name = project[:-4]
	# If collection doesn't have project
	if project_name not in current_entries:
		# Add project to table
		print("Adding", project_name)
		row = portfolioCollection.collection.add_row()
		row.name = project_name
		row.tag = 'Coding Projects'
		os.chdir(project_folder + '/' + project_name)
		row.link = process.communicate()[0].decode('utf-8').strip()
		with open(project_wiki_folder+'/'+project, 'r') as f:
			row.children.add_new(TextBlock, title=f.read())
	# If collection has project, but readme has been updated
	else:
		# Open new readme file as incoming
		with open(project_wiki_folder+'/'+project, 'r') as incoming:
			# reading from text file and splitting str_file into lines - delimited by "\n"
			file1_lines = incoming.read().split("\n")

			# Get the current readme from the wiki
		curr = portfolioCollection.collection.get_rows(
			search=project_name)[0].children[0].title
		file2_lines = curr.split("\n")

		# unique lines to each one, store it in their respective lists
		incoming_unique_file1 = []
		curr_unique_file2 = []

		# unique lines in str1
		for num, line1 in enumerate(file1_lines, 1):
			if line1 != '':
				if line1 not in file2_lines:
					incoming_unique_file1.append((line1, num))

		# unique lines in str2
		for num, line2 in enumerate(file2_lines, 1):
			if line2 != '':
				if line2 not in file1_lines:
					curr_unique_file2.append((line2, num))
		new_file = file2_lines

		if incoming_unique_file1 != [] and curr_unique_file2 != []:
			for line in incoming_unique_file1:
				# Add line to current that was already there
				new_file[line[1]-1] = line[0]

		elif incoming_unique_file1 == [] and curr_unique_file2 != []:
			for line in curr_unique_file2:
				# Remove line from current that no longer is there
				new_file.pop(line[1]-1)

		elif incoming_unique_file1 != [] and curr_unique_file2 == []:
			for line in incoming_unique_file1:
				# Add new line to current that is not there
				new_file.insert(line[1]-1, line[0])

		elif incoming_unique_file1 == [] and curr_unique_file2 == []:
			# Remove the old lines
			for line in curr_unique_file2:
				new_file[line[1]-1] = ''
				# Insert new ones
			for line in incoming_unique_file1:
				new_file.insert(line[1]-1, line[0])

		output = '\n'.join(new_file) + '\n'
		portfolioCollection.collection.get_rows(
			search=project_name)[0].children[0].title = output
