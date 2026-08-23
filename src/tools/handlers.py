from data.schema import COURSES, LECTURERS, SCHEDULES


def get_course_info(course_name: str) -> str:
    course_name = course_name.lower().strip()

    for key, course in COURSES.items():
        if (
            course_name == key.lower()
            or course_name in course.get("nama", "").lower()
            or course_name in course.get("kode", "").lower()
        ):
            return (
                f"Mata Kuliah: {course['nama']}\n"
                f"Kode: {course.get('kode', '-')}\n"
                f"SKS: {course['sks']}\n"
                f"Deskripsi: {course.get('deskripsi', '-')}\n"
                f"Semester: {course['semester']}"
            )

    return "Mata kuliah tidak ditemukan"


def get_lecturer_info(query: str) -> str:
    query = query.lower().strip()

    for key, lecturer in LECTURERS.items():
        lecturer_name = lecturer["nama"].lower().strip()
        taught_courses = [
            mk.lower().strip() for mk in lecturer.get("mk_yang_diampu", [])
        ]

        if query == lecturer_name or query in lecturer_name or query in taught_courses:
            mk_list = ", ".join(
                COURSES[mk]["nama"]
                for mk in lecturer["mk_yang_diampu"]
                if mk in COURSES
            )
            return (
                f"Dosen: {lecturer['nama'].strip()}\n"
                f"Email: {lecturer.get('email', '-')}\n"
                f"Keahlian: {', '.join(lecturer.get('keahlian', []))}\n"
                f"Mata Kuliah yang Diampu: {mk_list}"
            )

    return f"Dosen atau informasi untuk '{query}' tidak ditemukan."


def get_schedule(day: str = None, course_name: str = None) -> str:
    results = []

    if day:
        day = day.lower().strip()
    if course_name:
        course_name = course_name.lower().strip()

    for schedule in SCHEDULES:
        match = True

        if day and schedule["hari"].lower() != day:
            match = False

        if course_name:
            mk_key = schedule.get("mata_kuliah", "")
            mk_lower = mk_key.lower()
            if course_name != mk_lower and course_name not in mk_lower:
                match = False

        if match:
            mk_key = schedule.get("mata_kuliah", "")
            mk_info = COURSES.get(mk_key, {})
            mk_nama = mk_info.get("nama", mk_key)
            dosen_info = LECTURERS.get(schedule["dosen"], {})
            dosen_nama = dosen_info.get("nama", schedule.get("dosen", "-"))

            results.append(
                f"Hari: {schedule['hari'].capitalize()}\n"
                f"Jam: {schedule['jam']}\n"
                f"Ruangan: {schedule.get('ruangan', 'N/A')}\n"
                f"Mata Kuliah: {mk_nama}\n"
                f"Dosen: {dosen_nama}\n"
            )

    if results:
        return "\n---\n".join(results)

    return (
        "Jadwal tidak ditemukan. Pastikan parameter hari atau nama mata kuliah diisi."
    )


def execute_tool(tool_name: str, arguments: dict) -> str:
    try:
        if tool_name == "get_course_info":
            course_name = arguments.get("course_name", "")
            if not course_name:
                return "Error: Parameter 'course_name' diperlukan."
            return get_course_info(course_name)

        elif tool_name == "get_lecturer_info":
            query = arguments.get("query", "")
            if not query:
                return "Error: Parameter 'query' diperlukan."
            return get_lecturer_info(query)

        elif tool_name == "get_schedule":
            day = arguments.get("day")
            course_name = arguments.get("course_name")

            if not day and not course_name:
                return "Error: Minimal satu parameter harus diisi ('day' atau 'course_name')."

            return get_schedule(day=day, course_name=course_name)

        else:
            return f"Error: Tool '{tool_name}' tidak dikenali."

    except Exception as e:
        return f"Error executing tool: {str(e)}"
