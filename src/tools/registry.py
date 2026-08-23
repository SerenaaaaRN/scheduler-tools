TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "Mengambil detail mata kuliah berdasarkan nama atau kode MK.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "Nama atau kode mata kuliah (contoh: 'pemrograman_dasar' atau 'CS101')",
                    }
                },
                "required": ["course_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_lecturer_info",
            "description": "Mengambil profil dosen berdasarkan nama dosen atau mata kuliah yang diampu.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Nama dosen atau nama mata kuliah (contoh: 'budi_santoso' atau 'pemrograman_dasar')",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_schedule",
            "description": "Mengambil jadwal kelas dan ruangan berdasarkan hari atau nama mata kuliah.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Hari dalam seminggu (contoh: 'senin', 'selasa')",
                    },
                    "course_name": {
                        "type": "string",
                        "description": "Nama atau kode mata kuliah",
                    },
                },
                "required": [],
            },
        },
    },
]
