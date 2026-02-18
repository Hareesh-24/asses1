How It Works

Reads JSON file.

Cleans invalid values using clean_nan() function.

Checks if recipe title already exists.

If not exists → creates new record.

If exists → skips the record.

Displays number of created and skipped records.


Command Usage

Default file:

python manage.py load_recipes


Custom file:

python manage.py load_recipes --file=data.json



python manage.py sqlmigrate recipe_list 0001
BEGIN;
--
-- Create model Recipe
--
CREATE TABLE "recipe_list_recipe" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cuisine" text NOT NULL, "title" text NOT NULL, "rating" real NULL, "prep_time" integer NULL, "cook_time" integer NULL, "total_time" integer NULL, "description" text NOT NULL, "nutrients" text NULL CHECK ((JSON_VALID("nutrients") OR "nutrients" IS NULL)), "serves" text NULL);
COMMIT;

API Testing instructions

Endpoint 1: Get All Recipes
GET http://127.0.0.1:8000/api/recipes?page=1&limit=10

Endpoint 2: Search Recipes
GET http://127.0.0.1:8000/api/recipes/search?title=pie&rating=>=4.5&calories=<=400&cuisine=southern