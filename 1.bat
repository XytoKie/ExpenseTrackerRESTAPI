curl -X POST "http://127.0.0.1:5000/user" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":1234, \"name\": \"Jacob\" }"


curl -X POST "http://127.0.0.1:5000/user" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":2345, \"name\": \"Alice\" }"


curl -X POST "http://127.0.0.1:5000/user" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":3456, \"name\": \"Tom\" }"

curl -X POST "http://127.0.0.1:5000/category" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":4321, \"name\": \"Top-high\" }"


curl -X POST "http://127.0.0.1:5000/category" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":5432, \"name\": \"So-so\" }"

curl -X POST "http://127.0.0.1:5000/category" ^
     -H "Content-Type: application/json" ^
     -H "Accept: application/json" ^
     -v ^
     -d "{\"id\":6543, \"name\": \"Don't try this!\" }"


