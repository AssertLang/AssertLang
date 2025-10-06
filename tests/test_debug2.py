"""Debug new failing tests"""

from dsl.ir import *
from language.dotnet_generator_v2 import DotNetGeneratorV2, generate_csharp

# Test 1: Nullable types
print("=" * 60)
print("NULLABLE TYPES TEST:")
print("=" * 60)

cls = IRClass(
    name="user",
    properties=[
        IRProperty(name="id", prop_type=IRType(name="string")),
        IRProperty(name="age", prop_type=IRType(name="int", is_optional=True)),
    ],
)

module = IRModule(name="test", classes=[cls])
generator = DotNetGeneratorV2()
code = generator.generate(module)
print(code)
print()
print("Looking for: 'public int? Age'")
print("Found:", "public int? Age" in code)
print()

# Test 2: Full module
print("=" * 60)
print("FULL MODULE TEST:")
print("=" * 60)

module2 = IRModule(
    name="user_service",
    types=[
        IRTypeDefinition(
            name="user",
            fields=[
                IRProperty(name="id", prop_type=IRType(name="string")),
                IRProperty(name="name", prop_type=IRType(name="string")),
            ],
        )
    ],
    enums=[
        IREnum(
            name="status",
            variants=[
                IREnumVariant(name="active"),
                IREnumVariant(name="inactive"),
            ],
        )
    ],
    classes=[
        IRClass(
            name="user_repository",
            methods=[
                IRFunction(
                    name="get_user",
                    params=[IRParameter(name="id", param_type=IRType(name="string"))],
                    return_type=IRType(name="user"),
                    is_async=True,
                )
            ],
        )
    ],
)

generator2 = DotNetGeneratorV2()
code2 = generator2.generate(module2)
print(code2)
print()
print("Looking for: 'namespace UserService'")
print("Found:", "namespace UserService" in code2)
