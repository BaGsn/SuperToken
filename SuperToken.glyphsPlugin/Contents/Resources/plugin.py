# encoding: utf-8

###########################################################################################################
#
#
# General Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc, re, traceback
from GlyphsApp import Glyphs, EDIT_MENU, DOCUMENTWASSAVED
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSMenuItem, NSOnState, NSOffState
from Foundation import NSPredicate

class SuperToken(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.active = False
		self.name = Glyphs.localize({
			'en': 'Super Token'
		})

	@objc.python_method
	def start(self):
		# Create the menu item
		self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
			self.name, 
			self.togglePlugin_, 
			""
		)
		self.menuItem.setTarget_(self)
		Glyphs.menu[EDIT_MENU].append(self.menuItem)

	def togglePlugin_(self, sender):
		# Toggle the boolean state
		self.active = not self.active
		
		if self.active:
			# Enable: Add checkmark and callback
			self.menuItem.setState_(NSOnState)
			Glyphs.addCallback(self.runCallback, DOCUMENTWASSAVED)
			print("Super Token Enabled")
		else:
			# Disable: Remove checkmark and callback
			self.menuItem.setState_(NSOffState)
			# IMPORTANT: You must pass the same constant used to add it
			Glyphs.removeCallback(self.runCallback, DOCUMENTWASSAVED)
			print("Super Token Disabled")

	@objc.python_method
	def process_string(self, input_string):
		font = Glyphs.font

		pattern = r"\$(?:S)\[((?:[^'\]]+|'[^']*')+)\]"
		
		def replace_token(match):
			predicate_content = match.group(1)
			
			# Check for "replace X by Y" pattern
			replace_match = re.search(r"replace\s+'([^']+)'\s+by\s+'([^']*)'", predicate_content)
			
			# Check for "remove X" pattern
			remove_match = re.search(r"remove\s+'([^']+)'", predicate_content)
			
			if replace_match:
				# Extract the part before "replace" as the predicate
				predicate_part = predicate_content.split('replace')[0].strip()
				to_replace = replace_match.group(1)
				replace_with = replace_match.group(2)
				
				obj_c_predicate = predicate_part.replace('name', 'SELF')
				result = self.tokeniser(obj_c_predicate, to_replace, replace_with)

				# if result != input_string:
				return result
				
			elif remove_match:
				# Extract the part before "remove" as the predicate
				predicate_part = predicate_content.split('remove')[0].strip()
				to_remove = remove_match.group(1)
				
				obj_c_predicate = predicate_part.replace('name', 'SELF')
				result = self.tokeniser(obj_c_predicate, to_remove, '')
				# if result != input_string:
				return result
				
			else:
				# Default: no replacement, return names as-is
				obj_c_predicate = predicate_content.replace('name', 'SELF')
				result = self.tokeniser(obj_c_predicate, '', '')  # No replacement
				# if result != input_string:
				return result
		
		# Replace all matching patterns
		result = re.sub(pattern, replace_token, input_string)

		# if result != input_string:
		return result



	##################


	@objc.python_method
	def tokeniser(self, predicate, replace, replacement = ''):
		font = Glyphs.font
		
		# 1. Define the predicate to find names containing '.t-t'
		predicate = NSPredicate.predicateWithFormat_(predicate)
		
		# 2. Use the native Objective-C API to get and filter names
		names_array = font.glyphNames()
		filtered_names = names_array.filteredArrayUsingPredicate_(predicate)
		
		# Only replace if replace string is provided
		if replace:
			new_names = [n.replace(replace, replacement) for n in filtered_names]
		else:
			new_names = list(filtered_names)
		
		return ' '.join(new_names)


	#####################

	@objc.python_method
	def runCallback(self, info):
		font = Glyphs.font
		notes = ''
		processed_code = ''
		try:
			font.updateFeatures()

			for f_c in Glyphs.font.features + Glyphs.font.classes:
				if(not f_c.automatic and not f_c.name.startswith("ss")):

					notes = f_c.pyobjc_instanceMethods.notes()

					notes.replace('’','\'')

					if notes and isinstance(notes, str):  # Ensure it's a non-empty string
						print(f_c.name, notes)
						processed_code = self.process_string(notes)
						print(f_c.name, processed_code)
						
						if processed_code:
							# Replace code by generated code
							f_c.code = processed_code
					
							# Compile Opentype with the generated code
							font.compileFeatures()
							print('-')
						
		except:
			# Error. Print exception.
			print(traceback.format_exc())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
