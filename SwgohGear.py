from components.main_window import MainWindow

HEIGHT = 600
WIDTH = 900

def main():
  main = MainWindow()
  while True:
    if not main.is_running():
      break

if __name__ == '__main__':
  main()