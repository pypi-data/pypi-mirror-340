import re
from os import path
from glob import glob


def _get_pec(block):
    pec = re.search(r"`@pre_exercise_code`\n```{python}\n(.*?)\n```", block, re.DOTALL)
    return pec.group(1).strip() if pec else ""


def _get_key(block):
    key = re.search(r"key: ['\"']?([a-zA-Z0-9]+)['\"']?", block)
    return key.group(1) if key else None


def _get_solution(block):
    solution = re.search(r"`@solution`\n```{python}\n(.*?)\n```", block, re.DOTALL)
    return solution.group(1).strip() if solution else None


def _get_sct(block):
    sct = re.search(r"`@sct`\n```{python}\n(.*?)\n```", block, re.DOTALL)
    return sct.group(1).strip() if sct else None


def _get_name(block):
    name = re.search(r"^## (.*?)$", block, re.MULTILINE)
    return name.group(1).strip() if name else None


def _parse_exercise_blocks(content, chapter):
    exercises = []
    blocks = re.findall(r"## .*?(?=\n## |\Z)", content, re.DOTALL)

    for block in blocks:
        # Skip if not a NormalExercise or BulletExercise
        if not any(
            ex_type in block
            for ex_type in ["type: NormalExercise", "type: BulletExercise"]
        ):
            continue

        # Extract common fields
        name = _get_name(block)
        if not name:
            continue
        pec = _get_pec(block)
        key = _get_key(block)
        solution = _get_solution(block)
        sct = _get_sct(block)

        if "type: BulletExercise" in block:
            # Handle BulletExercise sub-blocks
            sub_blocks = re.findall(
                r"\*\*\*\n\n```yaml\ntype: NormalExercise.*?(?=\n\*\*\*|\Z)",
                block,
                re.DOTALL,
            )

            for sub_block in sub_blocks:
                sub_key = _get_key(sub_block)
                sub_solution = _get_solution(sub_block)
                sub_sct = _get_sct(sub_block)

                if all([sub_key, sub_solution, sub_sct]):
                    exercises.append(
                        _get_structured_exercise(
                            name, chapter, sub_key, sub_solution, sub_sct, pec
                        )
                    )
        elif all([key, solution, sct]):
            exercises.append(
                _get_structured_exercise(name, chapter, key, solution, sct, pec)
            )

    return exercises


def _get_structured_exercise(name, chapter, key, solution, sct, pec):
    return {
        "name": name,
        "chapter": chapter,
        "key": key,
        "solution": solution,
        "sct": sct,
        "pec": pec,
    }


def _get_chapter_exercises(chapter_path):
    try:
        chapter = re.search(r"chapter(\d+)\.md$", path.basename(chapter_path)).group(1)
        with open(chapter_path, "r", encoding="utf-8") as file:
            content = file.read()
        return _parse_exercise_blocks(content, chapter)
    except (FileNotFoundError, AttributeError) as e:
        print(f"Error processing {chapter_path}: {str(e)}")
        return []


def get_course_exercises(course_slug):
    base_path = path.join(path.dirname(__file__), "../../../courses", course_slug)

    try:
        base_path = path.abspath(base_path)
        chapter_files = glob(path.join(base_path, "chapter*.md"))
        if not chapter_files:
            print(f"No chapter files found in {base_path}")
            return []

        chapter_files.sort()

        exercises = []
        for chapter_file in chapter_files:
            chapter_exercises = _get_chapter_exercises(chapter_file)
            exercises.extend(chapter_exercises)
        return exercises
    except Exception as e:
        print(f"Error processing course {course_slug}: {str(e)}")
        return []
