# Recreating Synthetic Datasets

**Do not commit generated patient CSVs.** Store synthetic fixture outputs in the ignored `.project-vital/data/` directory and describe reproduction here.

From the **team repository root**:

```bash
python3 environment/data-testing/scripts/generate_data.py --level small --seed 42 --output .project-vital/data/small
python3 environment/data-testing/scripts/validate_data.py --input .project-vital/data/small
```

Repeat for `medium` and `large` with matching output directories. Document any team modifications, package versions, and additional validation commands.

| Level | Patients | Seed | Output location | Reproducibility evidence |
|---|---:|---:|---|---|
| Small | 200 | 42 | `.project-vital/data/small` | [path] |
| Medium | 2,000 | 42 | `.project-vital/data/medium` | [path] |
| Large | 20,000 | 42 | `.project-vital/data/large` | [path] |

Related encounter, appointment, and vital-sign counts must also be recorded and checked. Never use real patient data.
