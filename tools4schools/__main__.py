from tools4schools.test_app import app

#### Call the app
if __name__ == '__main__':
  app.run_server(host = '0.0.0.0', port = 5555, debug = False)