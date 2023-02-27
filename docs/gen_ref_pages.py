from pathlib import Path
import mkdocs_gen_files

# For the generation of a literate navigation file
nav = mkdocs_gen_files.Nav()

for path in sorted(Path("src").rglob("*.py")):  # 
    module_path = path.relative_to("src").with_suffix("")  # 
    print(module_path)
    doc_path = path.relative_to("src").with_suffix(".md")  # 
    print(doc_path)
    full_doc_path = Path("reference", doc_path)  # 
    print(full_doc_path)
    parts = list(module_path.parts)
    print(parts)
    print("-----")
    if parts[-1] == "__init__":  # 
        parts = parts[:-1]
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:  # 
        identifier = ".".join(parts)  # 
        print(":::src." + identifier, file=fd)  # 

    mkdocs_gen_files.set_edit_path(full_doc_path, path) 

# Writing the table of contents
with mkdocs_gen_files.open("reference/summary.md", "w") as nav_file:  # 
    nav_file.writelines(nav.build_literate_nav())