from fileFolderUI import FileFolderUI, FileExtensions



def process(path_element, list_elements):
    pass

# -------------------- Main code -------------------
if __name__ == "__main__":
    var = FileFolderUI()
    var.is_folder = False
    var.process_func = process
    var.files_extension = FileExtensions.DOCUMENTS
    var.run()
    
