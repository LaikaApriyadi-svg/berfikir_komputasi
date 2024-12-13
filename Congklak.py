
class CongklakGame:
    def __init__(self):
        # Papan congklak memiliki 7 lubang di setiap sisi
        # Setiap lubang awal diisi dengan 7 biji
        self.board = {
            'player1': [7] * 7,  # 7 lubang untuk Player 1
            'player2': [7] * 7,  # 7 lubang untuk Player 2
            'player1_home': 0,   # Lumbung/home Player 1
            'player2_home': 0    # Lumbung/home Player 2
        }
        self.current_player = 'player1'

    def display_board(self):
        """Menampilkan papan permainan"""
        print("\n--- PAPAN CONGKLAK ---")
        print("Player 2:", end=" ")
        print(" ".join(f"{x:2d}" for x in reversed(self.board['player2'])))
        print("Home Player 2:", self.board['player2_home'])
        print("Home Player 1:", self.board['player1_home'])
        print("Player 1:", " ".join(f"{x:2d}" for x in self.board['player1']))

    def is_game_over(self):
        """Memeriksa apakah permainan sudah berakhir"""
        return (sum(self.board['player1']) == 0) or (sum(self.board['player2']) == 0)

    def get_winner(self):
        """Menentukan pemenang"""
        if self.board['player1_home'] > self.board['player2_home']:
            return "Player 1"
        elif self.board['player2_home'] > self.board['player1_home']:
            return "Player 2"
        else:
            return "Seri"

    def move(self, player, hole_index):
        """Melakukan gerakan pada lubang tertentu"""
        # Pastikan lubang yang dipilih valid
        if hole_index < 0 or hole_index >= 7:
            print("Pilihan lubang tidak valid!")
            return False

        # Periksa apakah lubang memiliki biji
        if self.board[player][hole_index] == 0:
            print("Lubang kosong!")
            return False

        # Ambil biji dari lubang yang dipilih
        seeds = self.board[player][hole_index]
        self.board[player][hole_index] = 0
        current_player = player
        current_hole = hole_index

        # Distribusikan biji
        while seeds > 0:
            # Pindah ke lubang berikutnya
            current_hole += 1

            # Jika sudah melewati lubang terakhir pemain saat ini
            if current_hole >= 7:
                # Masukkan ke home/lumbung pemain
                if current_player == 'player1':
                    self.board['player1_home'] += 1
                else:
                    self.board['player2_home'] += 1
                seeds -= 1

                # Ganti pemain
                if current_player == 'player1':
                    current_player = 'player2'
                    current_hole = -1  # Siap untuk mulai dari awal sisi player2
                else:
                    current_player = 'player1'
                    current_hole = -1  # Siap untuk mulai dari awal sisi player1

                # Lanjutkan jika masih ada biji
                if seeds == 0:
                    break
                continue

            # Distribusikan biji ke lubang
            self.board[current_player][current_hole] += 1
            seeds -= 1

        # Periksa apakah biji terakhir jatuh di lubang kosong milik sendiri
        if (seeds == 0 and 
            self.board[current_player][current_hole] == 1 and 
            current_player == player):
            # Ambil biji dari lubang lawan di depannya
            opposite_hole = 6 - current_hole
            opposite_player = 'player2' if current_player == 'player1' else 'player1'
            
            if self.board[opposite_player][opposite_hole] > 0:
                # Tambahkan biji ke home pemain saat ini
                if current_player == 'player1':
                    self.board['player1_home'] += (
                        self.board[current_player][current_hole] + 
                        self.board[opposite_player][opposite_hole]
                    )
                else:
                    self.board['player2_home'] += (
                        self.board[current_player][current_hole] + 
                        self.board[opposite_player][opposite_hole]
                    )
                
                # Kosongkan lubang
                self.board[current_player][current_hole] = 0
                self.board[opposite_player][opposite_hole] = 0

        # Ganti giliran pemain
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
        return True

def main():
    game = CongklakGame()
    print("=== SELAMAT DATANG DI PERMAINAN CONGKLAK ===")
    print("Aturan:")
    print("1. Setiap pemain memiliki 7 lubang dengan 7 biji di setiap lubang")
    print("2. Tujuan: Mengumpulkan sebanyak mungkin biji di lumbung")
    print("3. Pilih lubang untuk mengambil dan menyebar biji")
    print("4. Jika biji terakhir di lubang sendiri, main lagi")
    print("5. Jika biji terakhir di lubang kosong milik sendiri, ambil biji lawan")

    while not game.is_game_over():
        # Tampilkan papan permainan
        game.display_board()

        # Input dari pemain
        try:
            print(f"\nGiliran {game.current_player}")
            hole = int(input("Pilih lubang (0-6): "))

            # Lakukan gerakan
            if not game.move(game.current_player, hole):
                continue
        except ValueError:
            print("Masukan tidak valid. Gunakan angka 0-6.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    # Tampilkan papan akhir
    game.display_board()

    # Tampilkan pemenang
    print(f"\nPemenang: {game.get_winner()}")
    print(f"Skor Lumbung Player 1: {game.board['player1_home']}")
    print(f"Skor Lumbung Player 2: {game.board['player2_home']}")

if __name__ == "__main__":
    main()
