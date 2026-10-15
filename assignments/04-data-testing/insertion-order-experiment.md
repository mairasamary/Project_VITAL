# Assignment 4 — Insertion Order and Referential Integrity

## 1. Relationship under investigation
**Parent entity/table:** [parent]  
**Child entity/table:** [child]  
**Linking fields:** [fields]  
**Expected order and why:** [evidence-supported expectation]

## 2. Baseline and safety
**Dedicated A4 project:** [name]  
**Starting state and query evidence:** [paths]  
Use only synthetic records in an isolated database.

## 3. Prediction
What will happen if the child is inserted **before** its expected parent? Separately predict (a) the SQL/database response and (b) the semantic validator's response. Do not assume a database foreign-key constraint exists without checking.

## 4. Controlled out-of-order attempt
| Step / command | Expected database response | Actual response | Evidence path |
|---|---|---|---|
| [command] | [prediction] | [observation] | [path] |

## 5. Integrity checks
| Check | Query / validator | Expected | Observed |
|---|---|---|---|
| Parent exists? | [query] | [result] | [result] |
| Child reference valid? | [query] | [result] | [result] |
| Semantic validation | [command] | [result] | [result] |

## 6. Conclusion and cleanup
Explain whether database acceptance matched the application's data-quality expectation. Document rollback/cleanup and limitations.
