"""Debug failing tests"""

from dsl.ir import *
from language.dotnet_generator_v2 import generate_csharp

# Test 1: Public API namespace
module = IRModule(
    name="simple",
    classes=[
        IRClass(
            name="hello",
            methods=[
                IRFunction(
                    name="world",
                    return_type=IRType(name="string"),
                    body=[
                        IRReturn(
                            value=IRLiteral(
                                value="Hello, World!",
                                literal_type=LiteralType.STRING,
                            )
                        )
                    ],
                )
            ],
        )
    ],
)

code = generate_csharp(module, namespace="MyApp")
print("=" * 60)
print("PUBLIC API TEST OUTPUT:")
print("=" * 60)
print(code)
print()

# Test 2: Full module
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

code2 = generate_csharp(module2)
print("=" * 60)
print("FULL MODULE TEST OUTPUT:")
print("=" * 60)
print(code2)
