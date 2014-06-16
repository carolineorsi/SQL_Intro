import pickle
from sql_problem import result_to_str, generate_result_hash
import sql_problem

PROBLEMS = [
{"instruction": """Write a query that shows all the information about all the salespeople in the database. Use a basic SELECT query.

    Examples: http://sqlzoo.net/wiki/SELECT_basics
    Syntax reference: http://sqlzoo.net/wiki/SELECT_Reference
""",
 "hint": """Select all the columns from the 'salespeople' table.""",
 "solution": """SELECT * FROM salespeople;"""},

{"instruction": """Write a query that shows all the information about all salespeople from the 'Northwest' region.

    Examples: http://sqlzoo.net/wiki/SELECT_basics
    Syntax reference: http://sqlzoo.net/wiki/SELECT_Reference
""",
 "hint": """Select all the columns from the 'salespeople' table where the region matches the string 'Northwest'.""",
 "solution": """SELECT * FROM salespeople WHERE region = 'Northwest';"""},

{"instruction": """Write a query that shows just the emails of the salespeople from the 'Southwest' region.

    Examples: http://sqlzoo.net/wiki/SELECT_basics
    Syntax reference: http://sqlzoo.net/wiki/SELECT_Reference
""",
 "hint": """Select the email column from the 'salespeople' table where the region matches the string 'Southwest'.""",
 "solution":  """SELECT email FROM salespeople WHERE region = 'Southwest';"""},

]

"""
SELECT givenname, surname, email FROM salespeople WHERE region = 'Northwest';
 -> After "SELECT" are the columns we want returned

 -> We can use * for everything
SELECT common_name FROM melons WHERE price > 5.0;
-> Melons that cost over $5

SELECT melon_type, common_name FROM melons WHERE price >= 5.0 AND melon_type = 'Watermelon';
-> Using an AND statement


SELECT common_name FROM melons WHERE common_name LIKE 'C%';
 - Starts with C
SELECT common_name FROM melons WHERE common_name LIKE '%Golden%';
 - Contains the word "Golden"

SELECT DISTINCT region FROM salespeople;
 -> get the individual regions

SELECT email FROM salespeople WHERE region = 'Northwest' OR region = 'Southwest';
vs.
SELECT email FROM salespeople WHERE region IN ('Northwest', 'Southwest');
 -> pick multiple regions

SELECT email, givenname, surname FROM salespeople WHERE region IN ('Northwest', 'Southwest') AND surname LIKE 'M%';
 -> Can combine with AND

SELECT melon_type, common_name, price, price*.735693 FROM melons;
 -> Convert melon price to Euros

--[Aggregate functions]--------
SELECT count(*) FROM customers;
 -> How many customers do we have?

SELECT count(*) FROM orders WHERE shipto_state = 'CA';
 -> How many orders were shipped to California?

SELECT SUM(order_total) FROM orders;
 -> dollar total for all orders

SELECT AVG(order_total) FROM orders;
 -> What is the average order amount?

SELECT MIN(order_total) FROM orders;
 -> What is the smallest (dollar amount) order?



SELECT id FROM customers WHERE email = 'sarah@geba.com';
 -> Get the customer id for sarah by email

SELECT id, status, order_total FROM orders WHERE customer_id = 100;
 -> Get the orders for sarah by customer id

--[ Nested SELECT ]-----------
SELECT id, status, order_total FROM orders WHERE customer_id = (SELECT id FROM customers WHERE email = 'sarah@geba.com'); 
 -> Get the orders for sarah by email address

--[JOINS]--------
SELECT O.id AS order_id, O.status, O.order_total, C.givenname, C.surname, C.email FROM orders O LEFT JOIN customers C ON (O.customer_id = C.id);
 -> Get all Orders with the customer name 

SELECT * FROM order_items WHERE order_id = 2724;
 -> What are all the items ordered for Order #2724?

SELECT M.common_name, M.melon_type, I.quantity, I.unit_price, I.total_price FROM order_items I LEFT JOIN melons M ON (I.melon_id = M.id) WHERE I.order_id = 2724;
 -> What are all the items ordered for Order #2724 with the melon details?


SELECT O.id, C.givenname, C.surname, O.shipto_address1, O.shipto_city, O.shipto_state, O.shipto_postalcode FROM orders O LEFT JOIN customers C ON (O.customer_id = C.id) WHERE status = 'New' AND O.shipto_state='CA';
 -> Get shipping details for all new orders in CA

SELECT I.melon_id, I.quantity, M.melon_type, M.common_name FROM order_items I LEFT JOIN melons M ON (I.melon_id = M.id) WHERE order_id IN (SELECT O.id FROM orders O  WHERE status = 'New' AND O.shipto_state='CA');
 -> Get all melons ordered for new orders in CA


SELECT I.melon_id, SUM(I.quantity), M.melon_type, M.common_name FROM order_items I LEFT JOIN melons M ON (I.melon_id = M.id) WHERE order_id IN (SELECT O.id FROM orders O  WHERE status = 'New' AND O.shipto_state='CA') GROUP BY I.melon_id;
 -> Get the total number of each type of melon for new orders in CA


SELECT S.givenname, S.surname, SUM(order_total), SUM(order_total) * .15 AS commision FROM salespeople S LEFT JOIN orders O ON (O.salesperson_id = S.id) GROUP BY S.id;
 -> Get a list of all sales people and the total amount of orders they've sold.  Calculate a 15% commision.

SELECT SUM(order_total) FROM orders WHERE salesperson_id IS NULL;
 -> Get total amount of web orders (no sales person id) 
"""

def generate_solution_hash(problem, cursor):
    soln_query = problem['solution']
    return generate_result_hash(soln_query, cursor)

def serialize_problems(problems, cursor):
    for p in problems:
        hash_ = generate_solution_hash(p, cursor)
        p['soln_hash'] = hash_
        del p['solution']

    output_file = open("problem_set.pickle", "w")
    pickle.dump(problems, output_file)
    

def main():
    cursor = sql_problem.connect()
    output = serialize_problems(PROBLEMS, cursor)


if __name__ == "__main__":
    main()


