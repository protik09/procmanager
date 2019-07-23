import os
from gi.repository import Gtk, WebKit


class WYSIWYG(Gtk.VBox):
	def __init__(self, window):
		Gtk.VBox.__init__(self)
		self.window = window
		self.editor = WebKit.WebView()
		self.editor.set_editable(True)
		self.editor.load_html_string("", "file:///")

		scroll = Gtk.ScrolledWindow()
		scroll.add(self.editor)
		scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

		self.ui = self.generate_ui()
		self.toolbar1 = self.ui.get_widget("/toolbar_main")
		self.toolbar2 = self.ui.get_widget("/toolbar_format")

		self.pack_start(self.toolbar2, False, True, 0)
		self.pack_start(scroll, True, True, 0)

	def generate_ui(self):
		ui_def = """
		<ui>
		  <toolbar name="toolbar_format">
			<toolitem action="bold" />
			<toolitem action="italic" />
			<toolitem action="underline" />
			<toolitem action="strikethrough" />
			<separator />
			<toolitem action="font" />
			<toolitem action="color" />
			<separator />
			<toolitem action="justifyleft" />
			<toolitem action="justifyright" />
			<toolitem action="justifycenter" />
			<toolitem action="justifyfull" />
			<separator />
			<toolitem action="insertimage" />
			<toolitem action="insertlink" />
		  </toolbar>
		</ui>
		"""

		actions = Gtk.ActionGroup("Actions")
		actions.add_actions([
			("menuInsert", None, "_Insert"),
			("menuFormat", None, "_Format"),

			("bold", Gtk.STOCK_BOLD, "_Bold", "<ctrl>B", None, self.on_action),
			("italic", Gtk.STOCK_ITALIC, "_Italic",
			 "<ctrl>I", None, self.on_action),
			("underline", Gtk.STOCK_UNDERLINE,
			 "_Underline", "<ctrl>U", None, self.on_action),
			("strikethrough", Gtk.STOCK_STRIKETHROUGH,
			 "_Strike", "<ctrl>T", None, self.on_action),
			("font", Gtk.STOCK_SELECT_FONT, "Select _Font",
			 "<ctrl>F", None, self.on_select_font),
			("color", Gtk.STOCK_SELECT_COLOR, "Select _Color",
			 None, None, self.on_select_color),

			("justifyleft", Gtk.STOCK_JUSTIFY_LEFT,
			 "Justify _Left", None, None, self.on_action),
			("justifyright", Gtk.STOCK_JUSTIFY_RIGHT,
			 "Justify _Right", None, None, self.on_action),
			("justifycenter", Gtk.STOCK_JUSTIFY_CENTER,
			 "Justify _Center", None, None, self.on_action),
			("justifyfull", Gtk.STOCK_JUSTIFY_FILL,
			 "Justify _Full", None, None, self.on_action),

			("insertimage", "insert-image", "Insert _Image",
			 None, None, self.on_insert_image),
			("insertlink", "insert-link", "Insert _Link",
			 None, None, self.on_insert_link),
		])
		actions.get_action("insertimage").set_property(
			"icon-name", "insert-image")
		actions.get_action("insertlink").set_property(
			"icon-name", "insert-link")

		ui = Gtk.UIManager()
		ui.insert_action_group(actions)
		ui.add_ui_from_string(ui_def)
		return ui

	def on_action(self, action):
		self.editor.execute_script(
			"document.execCommand('%s', false, false);" % action.get_name())

	def on_paste(self, action):
		self.editor.paste_clipboard()

	def on_new(self, action):
		self.editor.load_html_string("", "file:///")

	def on_select_font(self, action):
		dialog = Gtk.FontSelectionDialog("Select a font")
		if dialog.run() == Gtk.ResponseType.OK:
			fontsel = dialog.get_font_selection()
			self.editor.execute_script(
				"document.execCommand('fontname', null, '%s');" % fontsel.get_family().get_name())
			self.editor.execute_script(
				"document.execCommand('fontsize', null, '%s');" % fontsel.get_size())
		dialog.destroy()

	def on_select_color(self, action):
		dialog = Gtk.ColorSelectionDialog("Select Color")
		if dialog.run() == Gtk.ResponseType.OK:
			color = dialog.get_color_selection().get_current_color()
			rgba = dialog.get_color_selection().get_current_rgba()
			color = '#%02x%02x%02x' % (
				rgba.red * 256, rgba.green * 256, rgba.blue * 256)
			self.editor.execute_script(
				"document.execCommand('forecolor', null, '%s');" % color)
		dialog.destroy()

	def on_insert_link(self, action):
		dialog = Gtk.Dialog("Enter a URL:", self.window, 0,
							(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

		entry = Gtk.Entry()
		dialog.vbox.pack_start(entry, True, True, 0)
		dialog.show_all()

		if dialog.run() == Gtk.ResponseType.OK:
			self.editor.execute_script(
				"document.execCommand('createLink', true, '%s');" % entry.get_text())
		dialog.destroy()

	def on_insert_image(self, action):
		dialog = Gtk.FileChooserDialog("Select an image file", self.window, Gtk.FileChooserAction.OPEN,
									   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		if dialog.run() == Gtk.ResponseType.OK:
			fn = dialog.get_filename()
			if os.path.exists(fn):
				self.editor.execute_script(
					"document.execCommand('insertImage', null, '%s');" % fn)
		dialog.destroy()

	def get_html(self):
		self.editor.execute_script(
			"document.title=document.documentElement.innerHTML;")
		html = self.editor.get_main_frame().get_title()
		self.editor.execute_script("document.title='';")
		return html


if __name__ == '__main__':
	w = Gtk.Window()
	w.set_title("Example Editor")
	w.connect("destroy", Gtk.main_quit)
	w.resize(800, 800)
	wysiwyg = WYSIWYG(w)
	w.add(wysiwyg)
	w.show_all()
	Gtk.main()
