import unittest
import subprocess

def run_script(commands):
    process = subprocess.Popen("./db", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, _ = process.communicate("\n".join(commands) + "\n")
    return stdout.strip().split("\n")

class TestDatabase(unittest.TestCase):
    
    def test_insert_and_retrieve(self):
        result = run_script([
            "insert 1 user1 person1@example.com",
            "select",
            ".exit",
        ])
        self.assertEqual(result, [
            "db > Executed.",
            "db > (1, user1, person1@example.com)",
            "Executed.",
            "db > "
        ])
    
    def test_table_full_error(self):
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1402)]
        script.append(".exit")
        result = run_script(script)
        self.assertEqual(result[-2], "db > Error: Table full.")
    
    def test_max_length_strings(self):
        long_username = "a" * 32
        long_email = "a" * 255
        result = run_script([
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ])
        self.assertEqual(result, [
            "db > Executed.",
            f"db > (1, {long_username}, {long_email})",
            "Executed.",
            "db > "
        ])
    
    def test_too_long_strings_error(self):
        long_username = "a" * 33
        long_email = "a" * 256
        result = run_script([
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ])
        self.assertEqual(result, [
            "db > String is too long.",
            "db > Executed.",
            "db > "
        ])
    
    def test_negative_id_error(self):
        result = run_script([
            "insert -1 cstack foo@bar.com",
            "select",
            ".exit",
        ])
        self.assertEqual(result, [
            "db > ID must be positive.",
            "db > Executed.",
            "db > "
        ])

if __name__ == "__main__":
    unittest.main()

