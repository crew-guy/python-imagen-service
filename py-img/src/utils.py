def delete_file(file):
    try:
        import os
        os.remove(file)
    except:
        pass