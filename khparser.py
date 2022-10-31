class ScriptAnalyzer:

    found_words = {}

    exclusion_list = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me"]
    script_list = []

    def __init__(self, path='C:/Users/minouye/Desktop/kh.txt'):
        script_list = []
        found_words = {}
        exclusion_list = self.exclusion_list
        
        with open(path, 'r') as file:
            for line in file:
                # Only consider lines with dialogue in them
                if ":" not in line:
                    continue

                speaker_line_split_arr = line.split(":", 1)
                
                speaker_name_char_arr = []
                # Omit characters in parentheses, non-alphanumerics like punctuation
                open_par_count = 0
                for c in speaker_line_split_arr[0]:
                    if c == "(":
                        open_par_count += 1
                    elif c == ")":
                        open_par_count -= 1
                    elif (c.isalnum() or c == " ") and open_par_count <= 0:
                        speaker_name_char_arr.append(c.lower())
                speaker_words_only_str = ''.join(speaker_name_char_arr)
                
                open_par_count = 0
                line_char_arr = []
                for c in speaker_line_split_arr[1]:
                    if c == "(":
                        open_par_count += 1
                    elif c == ")":
                        open_par_count -= 1
                    elif (c.isalnum() or c == " ") and open_par_count <= 0:
                        line_char_arr.append(c.lower())
                        
                words_only_str = ''.join(line_char_arr)
                words_arr = words_only_str.split(" ")
                script_list.append([speaker_words_only_str, words_arr])

                # Filter for speaker
                '''
                if words_arr[0] != "sora":
                    continue
                '''
                '''
                if words_arr[0] == "kairi":
                    if "kairi (speaker)" not in found_words:
                        found_words["kairi (speaker)"] = 1
                    else:
                        found_words["kairi (speaker)"] += 1
                    continue
                '''

        self.script_list = script_list
        
            
    def compute_word_frequency(self, speaker=""):
        # Bring class variables into scope because Python is stupid
        script_list = self.script_list
        found_words = self.found_words
        exclusion_list = self.exclusion_list
        
        for line in script_list:
            # If speaker was specified, skip lines by other people
            if speaker and line[0] != speaker:
                continue

            for word in line[1]:
                if word not in exclusion_list:
                    if word not in found_words:
                        found_words[word] = 1
                    else:
                        found_words[word] += 1

        ranking_dict = {}
        for word in found_words:
            if found_words[word] not in ranking_dict:
                ranking_dict[found_words[word]] = [word]
            else:
                ranking_dict[found_words[word]].append(word)

        found_max = 0
        for rank in ranking_dict:
            if rank > found_max:
                found_max = rank
        i = 0
        print(found_max)
        while i < 100 and found_max > 0:
            if found_max in ranking_dict:
                print(f"{found_max}: {ranking_dict[found_max]}")
                i += len(ranking_dict[found_max])
            found_max -= 1

    # Count lines that contain words
    def count_lines_containing(self, speaker="sora", key="heart"):
        script_list = self.script_list
        line_count = 0
        key_count = 0

        for line in script_list:
            if line[0] == speaker:
                line_count += 1
                if key in line[1]:
                    key_count += 1
                    print(" ".join(line[1]), "\n")

        print(f"Out of {line_count} lines {speaker} references {key} {key_count} times.")

        user_input = ""
        while user_input != "quit":
            user_input = input("query: ")
            if user_input in found_words:
                print(found_words[user_input])
        
print("Starting")
new_script_analyzer = ScriptAnalyzer()
new_script_analyzer.compute_word_frequency()
new_script_analyzer.count_lines_containing()

