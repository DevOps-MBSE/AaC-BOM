# Material-Model

## Plugin Commands


### Command: gen-bom

Generates a CSV Bill-of-Materials (BOM) from a list of site models.

Example shell usage:

```bash
(.env) $ aac gen-bom -h
```

#### Command arguments

- `-h`, `--help`: Shows a help message
- `architecture-file` (`str`): The deployment model to convert into a BOM.- `output-directory` (`str`): The directory where the BOM file should be placed.

## Plugin Extensions and Definitions


### Validation - Referenced materials exist

TODO: Add descriptive information about Referenced materials exist

```yaml
validation:
  name: Referenced materials exist
  description: Verifies names within deployment, assembly, and part references exist
    within the context.
  behavior:
  - name: Verify that part references exist.
    type: request-response
    description: null
    input:
    - name: input
      type: ValidatorInput
    output:
    - name: results
      type: ValidatorOutput
    acceptance:
    - scenario: Successfully Validate a part reference name exists
      given:
      - The ValidatorInput content consists of valid AaC definitions.
      - The ValidatorInput contains some AaC fields that reference requirement ids.
      when:
      - The input is validation
      then:
      - The ValidatorOutput does not indicate any errors
      - The ValidatorOutput does not indicate any warnings
      - The ValidatorOutput indicates the definition under test is valid
    - scenario: Fail to validate a definition&#39;s requirement reference fields
      given:
      - The ValidatorInput content consists of otherwise valid AaC definitions.
      - The ValidatorInput contains at least one requirement reference id that does
        not exist.
      when:
      - The ValidatorInput is validated
      then:
      - The ValidatorOutput has errors
      - The ValidatorOutput errors indicate that there are invalid requirement id
        references

```

### Validation - No circular material references

TODO: Add descriptive information about No circular material references

```yaml
validation:
  name: No circular material references
  description: Verifies the references within bill of material models form a directed
    acyclic graph.
  behavior:
  - name: Verify that no circular references exist.
    type: request-response
    description: null
    input:
    - name: input
      type: ValidatorInput
    output:
    - name: results
      type: ValidatorOutput
    acceptance:
    - scenario: Successfully Validate a no circular references exist
      given:
      - The ValidatorInput content consists of valid AaC definitions.
      - The ValidatorInput contains some AaC fields that reference requirement ids.
      when:
      - The input is validation
      then:
      - The ValidatorOutput does not indicate any errors
      - The ValidatorOutput does not indicate any warnings
      - The ValidatorOutput indicates the definition under test is valid
    - scenario: Fail to validate a definition&#39;s requirement reference fields
      given:
      - The ValidatorInput content consists of otherwise valid AaC definitions.
      - The ValidatorInput contains at least one requirement reference id that does
        not exist.
      when:
      - The ValidatorInput is validated
      then:
      - The ValidatorOutput has errors
      - The ValidatorOutput errors indicate that there are invalid requirement id
        references

```

### Ext - MaterialRootItems

TODO: Add descriptive information about MaterialRootItems

```yaml
ext:
  name: MaterialRootItems
  type: Root
  schemaExt:
    add:
    - name: part
      type: Part
    - name: assembly
      type: Assembly
    - name: site
      type: Site

```

### Schema - Part

TODO: Add descriptive information about Part

```yaml
schema:
  name: Part
  description: A material item used in a system (hardware, software, or service).
  fields:
  - name: name
    type: string
    description: Unique name of the part
  - name: make
    type: string
    description: The source supplier
  - name: model
    type: string
    description: The source supplier&#39;s model number
  - name: description
    type: string
    description: A short description of the part
  - name: unit_cost
    type: number
    description: The cost of this item
  - name: lead_time
    type: int
    description: The quoted or estimated lead time to receive the part once put on
      order (in days)
  - name: quote_type
    type: QuoteType
    description: How the unit cost (and probably lead time) was obtained
  - name: quote_source
    type: string
    description: Pointer to material supporting the unit cost. Quote type will have
      a bearing on field content.
  validation:
  - name: Required fields are present
    arguments:
    - name
    - make
    - model
    - description
    - unit_cost

```

### Schema - PartRef

TODO: Add descriptive information about PartRef

```yaml
schema:
  name: PartRef
  description: Reference to a part with quantity
  fields:
  - name: part-ref
    type: reference
    description: Reference fo the name in a Part item.
  - name: quantity
    type: int
    description: The count of the parts to be used.
  validation:
  - name: Required fields are present
    arguments:
    - part-ref
    - quantity
  - name: Referenced materials exist
    arguments:
    - part-ref

```

### Schema - Assembly

TODO: Add descriptive information about Assembly

```yaml
schema:
  name: Assembly
  description: A collection of parts into a logical thing.
  fields:
  - name: name
    type: string
    description: The unique name of the assembly.
  - name: description
    type: string
    description: A description of the assembly.
  - name: parts
    type: PartRef[]
    description: A list of parts that contribute to the assembly.
  - name: sub-assemblies
    type: AssemblyRef[]
    description: A list of assemblies that contribute to the assembly.
  validation:
  - name: Required fields are present
    arguments:
    - name
    - description

```

### Schema - AssemblyRef

TODO: Add descriptive information about AssemblyRef

```yaml
schema:
  name: AssemblyRef
  description: Reference to an assembly with quantity
  fields:
  - name: assembly-ref
    type: reference
    description: Reference fo the name in another Assembly item.
  - name: quantity
    type: int
    description: The count of the assemblies to be used.
  validation:
  - name: Required fields are present
    arguments:
    - assembly-ref
    - quantity
  - name: Referenced materials exist
    arguments:
    - assembly-ref
  - name: No circular material references

```

### Schema - Site

TODO: Add descriptive information about Site

```yaml
schema:
  name: Site
  description: A collection of parts and assemblies to be deployed to one or more
    locations.
  fields:
  - name: name
    type: string
    description: The unique name of the site.
  - name: description
    type: string
    description: A description of the site.
  - name: location
    type: string
    description: The location for the site.
  - name: parts
    type: PartRef[]
    description: A list of parts that contribute to the site.
  - name: assemblies
    type: AssemblyRef[]
    description: A list of assemblies that contribute to the site.
  - name: sub-site
    type: SiteRef[]
    description: A list of sites that contribute to this site (i.e. buildings on a
      campus, rooms in a building).
  - name: need_date
    type: date
    descriptioN: Optional field to define a needed material receive date.
  validation:
  - name: Required fields are present
    arguments:
    - name
    - description
    - location
  - name: No circular material references

```

### Schema - SiteRef

TODO: Add descriptive information about SiteRef

```yaml
schema:
  name: SiteRef
  description: Reference to a site with quantity
  fields:
  - name: site-ref
    type: reference
    description: Reference to another Site item.
  - name: quantity
    type: int
    description: The number of sites to include.
  validation:
  - name: Required fields are present
    arguments:
    - site-ref
    - quantity
  - name: Referenced materials exist
    arguments:
    - site-ref

```

### Enum - QuoteType

TODO: Add descriptive information about QuoteType

```yaml
enum:
  name: QuoteType
  values:
  - Engineering_Estimate
  - Vendor_Quote
  - Web_Reference
  - Furnished_Equipment
  - Reuse

```
