import random, unicodedata, os, re, unicodedata

class WordBank:

    all_words : list[str]
    valid_words : set
    available_words : list

    def __init__(self, archive_path : str):
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Arquivo de palavras não encontrado: {archive_path}.")
        
        all_words = self._read_archive(archive_path)

        self.valid_words = self._filter_valid_words(all_words)
        self.available_words = list(self.valid_words)

        if len(self.valid_words) == 0:
            raise ValueError(f"Nenhuma palavra válida de 5 letras foi encontrada em: {archive_path}.")

    def _read_archive(self, archive_path : str) -> list[str]:
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()

            return re.findall(r'[a-zA-ZÀ-ú]+', content)

    def _normalize_word(self, word : str) -> str:
        normalized : str = unicodedata.normalize('NFD', word)
        no_accent : str = normalized.encode('ascii', 'ignore').decode('utf8')

        return no_accent.upper()

    def _filter_valid_words(self, all_words : list[str]) -> set[str]:
        clear_words : set[str] = set()

        for word in all_words:
            if len(word) == 5:
                normalized_word : str = self._normalize_word(word)

                if len(normalized_word) == 5 and normalized_word.isalpha():
                    clear_words.add(normalized_word)
        
        return clear_words

    def get_random_word(self) -> str:
        if not self.available_words:
            if not self._reset_available_words():
                return "ERRO"
        
        word = random.choice(self.available_words)
        self.available_words.remove(word)

        return word

    def _reset_available_words(self) -> bool:        
        self.available_words = list(self.valid_words)

        if not self.available_words:
            return False
    
        return True

    def is_valid_word(self, word : str) -> bool:
        normalized_word = self._normalize_word(word)
        return normalized_word in self.valid_words


# --- Testes ---

if __name__ == "__main__":
    
    print("--- Testando BancoDePalavras ---")
    
    try:
        bank = WordBank("words.txt")
        print(f"Carregadas {len(bank.valid_words)} palavras válidas.")
        print(f"Exemplos: {list(bank.valid_words)[:5]}")
        
        print(f"\n'TESTE' é válida? {bank.is_valid_word('TESTE')}")
        print(f"'causa' é válida? {bank.is_valid_word('causa')}")
        print(f"'ABCDE' é válida? {bank.is_valid_word('ABCDE')}")
        
        print("\nPegando 3 palavras aleatórias:")
        print(f"1. {bank.get_random_word()}")
        print(f"2. {bank.get_random_word()}")
        print(f"3. {bank.get_random_word()}")
        
        print(f"\nPalavras restantes disponíveis: {len(bank.available_words)}")

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)