"""
.NET Generator V2 Demo

Demonstrates the IR → C# code generation capabilities.
"""

from dsl.ir import *
from language.dotnet_generator_v2 import generate_csharp


def demo_simple_class():
    """Demo: Generate a simple class with properties."""
    print("=" * 60)
    print("DEMO 1: Simple Class with Properties")
    print("=" * 60)

    module = IRModule(
        name="user_service",
        types=[
            IRTypeDefinition(
                name="user",
                doc="Represents a user in the system",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="string")),
                    IRProperty(name="name", prop_type=IRType(name="string")),
                    IRProperty(name="email", prop_type=IRType(name="string", is_optional=True)),
                    IRProperty(name="age", prop_type=IRType(name="int", is_optional=True)),
                ],
            )
        ],
    )

    code = generate_csharp(module)
    print(code)


def demo_async_method():
    """Demo: Generate async method with Task<T>."""
    print("=" * 60)
    print("DEMO 2: Async Method with Database Call")
    print("=" * 60)

    module = IRModule(
        name="repository",
        classes=[
            IRClass(
                name="user_repository",
                properties=[
                    IRProperty(
                        name="connection_string",
                        prop_type=IRType(name="string"),
                        is_private=True,
                    )
                ],
                methods=[
                    IRFunction(
                        name="get_user_by_id",
                        params=[IRParameter(name="id", param_type=IRType(name="string"))],
                        return_type=IRType(name="User"),
                        is_async=True,
                        doc="Fetches a user from the database asynchronously",
                        body=[
                            IRAssignment(
                                target="query",
                                value=IRLiteral(
                                    value="SELECT * FROM Users WHERE Id = @id",
                                    literal_type=LiteralType.STRING,
                                ),
                                is_declaration=True,
                            ),
                            IRReturn(
                                value=IRCall(
                                    function=IRPropertyAccess(
                                        object=IRIdentifier(name="database"),
                                        property="query_async",
                                    ),
                                    args=[IRIdentifier(name="query")],
                                )
                            ),
                        ],
                    ),
                    IRFunction(
                        name="create_user",
                        params=[
                            IRParameter(name="user", param_type=IRType(name="User")),
                        ],
                        is_async=True,
                        return_type=IRType(name="bool"),
                        body=[
                            IRReturn(
                                value=IRCall(
                                    function=IRPropertyAccess(
                                        object=IRIdentifier(name="database"),
                                        property="insert_async",
                                    ),
                                    args=[IRIdentifier(name="user")],
                                )
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    code = generate_csharp(module)
    print(code)


def demo_control_flow():
    """Demo: Generate control flow (if/for/try-catch)."""
    print("=" * 60)
    print("DEMO 3: Control Flow with Validation")
    print("=" * 60)

    module = IRModule(
        name="validator",
        classes=[
            IRClass(
                name="user_validator",
                methods=[
                    IRFunction(
                        name="validate",
                        params=[IRParameter(name="user", param_type=IRType(name="User"))],
                        return_type=IRType(name="bool"),
                        throws=["ValidationException"],
                        body=[
                            # Check if user is null
                            IRIf(
                                condition=IRBinaryOp(
                                    op=BinaryOperator.EQUAL,
                                    left=IRIdentifier(name="user"),
                                    right=IRLiteral(value=None, literal_type=LiteralType.NULL),
                                ),
                                then_body=[
                                    IRThrow(
                                        exception=IRCall(
                                            function=IRIdentifier(name="ValidationException"),
                                            args=[
                                                IRLiteral(
                                                    value="User cannot be null",
                                                    literal_type=LiteralType.STRING,
                                                )
                                            ],
                                        )
                                    )
                                ],
                            ),
                            # Check name length
                            IRIf(
                                condition=IRBinaryOp(
                                    op=BinaryOperator.LESS_THAN,
                                    left=IRPropertyAccess(
                                        object=IRPropertyAccess(
                                            object=IRIdentifier(name="user"),
                                            property="name",
                                        ),
                                        property="length",
                                    ),
                                    right=IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                                ),
                                then_body=[
                                    IRReturn(
                                        value=IRLiteral(
                                            value=False, literal_type=LiteralType.BOOLEAN
                                        )
                                    )
                                ],
                            ),
                            # All valid
                            IRReturn(
                                value=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN)
                            ),
                        ],
                    )
                ],
            )
        ],
    )

    code = generate_csharp(module)
    print(code)


def demo_enum_and_types():
    """Demo: Generate enums and type definitions."""
    print("=" * 60)
    print("DEMO 4: Enums and Type Definitions")
    print("=" * 60)

    module = IRModule(
        name="models",
        enums=[
            IREnum(
                name="user_status",
                doc="User account status",
                variants=[
                    IREnumVariant(name="active", value=1),
                    IREnumVariant(name="suspended", value=2),
                    IREnumVariant(name="deleted", value=3),
                ],
            ),
            IREnum(
                name="user_role",
                variants=[
                    IREnumVariant(name="admin"),
                    IREnumVariant(name="moderator"),
                    IREnumVariant(name="user"),
                ],
            ),
        ],
        types=[
            IRTypeDefinition(
                name="user_profile",
                fields=[
                    IRProperty(name="user_id", prop_type=IRType(name="string")),
                    IRProperty(
                        name="status",
                        prop_type=IRType(name="user_status"),
                    ),
                    IRProperty(
                        name="role",
                        prop_type=IRType(name="user_role"),
                    ),
                    IRProperty(
                        name="created_at",
                        prop_type=IRType(name="string"),  # DateTime in real world
                    ),
                ],
            )
        ],
    )

    code = generate_csharp(module)
    print(code)


def demo_full_application():
    """Demo: Complete application with multiple classes."""
    print("=" * 60)
    print("DEMO 5: Complete E-Commerce Application")
    print("=" * 60)

    module = IRModule(
        name="ecommerce",
        types=[
            IRTypeDefinition(
                name="product",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="string")),
                    IRProperty(name="name", prop_type=IRType(name="string")),
                    IRProperty(name="price", prop_type=IRType(name="float")),
                    IRProperty(name="stock", prop_type=IRType(name="int")),
                ],
            ),
            IRTypeDefinition(
                name="order",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="string")),
                    IRProperty(name="user_id", prop_type=IRType(name="string")),
                    IRProperty(
                        name="items",
                        prop_type=IRType(
                            name="array",
                            generic_args=[IRType(name="product")],
                        ),
                    ),
                    IRProperty(name="total", prop_type=IRType(name="float")),
                ],
            ),
        ],
        enums=[
            IREnum(
                name="order_status",
                variants=[
                    IREnumVariant(name="pending"),
                    IREnumVariant(name="processing"),
                    IREnumVariant(name="shipped"),
                    IREnumVariant(name="delivered"),
                ],
            )
        ],
        classes=[
            IRClass(
                name="order_service",
                methods=[
                    IRFunction(
                        name="create_order",
                        params=[
                            IRParameter(name="user_id", param_type=IRType(name="string")),
                            IRParameter(
                                name="products",
                                param_type=IRType(
                                    name="array",
                                    generic_args=[IRType(name="product")],
                                ),
                            ),
                        ],
                        return_type=IRType(name="order"),
                        is_async=True,
                        body=[
                            # Calculate total
                            IRAssignment(
                                target="total",
                                value=IRLiteral(value=0.0, literal_type=LiteralType.FLOAT),
                                is_declaration=True,
                            ),
                            # Return new order
                            IRReturn(
                                value=IRCall(
                                    function=IRIdentifier(name="Order"),
                                    args=[],
                                )
                            ),
                        ],
                    )
                ],
            )
        ],
    )

    code = generate_csharp(module, namespace="MyCompany.ECommerce")
    print(code)


if __name__ == "__main__":
    demos = [
        demo_simple_class,
        demo_async_method,
        demo_control_flow,
        demo_enum_and_types,
        demo_full_application,
    ]

    for demo in demos:
        demo()
        print("\n")
