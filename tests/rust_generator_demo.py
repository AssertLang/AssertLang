"""
Comprehensive Demo of Rust Generator V2

Shows all major features and generates a complete Rust module.
"""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

from language.rust_generator_v2 import generate_rust
from dsl.ir import (
    IRModule,
    IRImport,
    IRFunction,
    IRParameter,
    IRType,
    IRTypeDefinition,
    IRProperty,
    IREnum,
    IREnumVariant,
    IRClass,
    IRReturn,
    IRAssignment,
    IRIf,
    IRFor,
    IRLiteral,
    IRIdentifier,
    IRBinaryOp,
    IRCall,
    IRArray,
    IRPropertyAccess,
    BinaryOperator,
    LiteralType,
)


def create_comprehensive_module() -> IRModule:
    """Create a comprehensive IR module showcasing all features."""

    module = IRModule(name="user_service", version="1.0.0")

    # =========================================================================
    # 1. Type Definitions (Structs)
    # =========================================================================

    # User struct
    user_struct = IRTypeDefinition(
        name="User",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="username", prop_type=IRType(name="string")),
            IRProperty(name="email", prop_type=IRType(name="string", is_optional=True)),
            IRProperty(name="age", prop_type=IRType(name="int")),
            IRProperty(name="active", prop_type=IRType(name="bool")),
        ],
        doc="Represents a user in the system"
    )
    module.types.append(user_struct)

    # UserStats struct with collections
    stats_struct = IRTypeDefinition(
        name="UserStats",
        fields=[
            IRProperty(
                name="tags",
                prop_type=IRType(
                    name="array",
                    generic_args=[IRType(name="string")]
                )
            ),
            IRProperty(
                name="metadata",
                prop_type=IRType(
                    name="map",
                    generic_args=[
                        IRType(name="string"),
                        IRType(name="int")
                    ]
                )
            ),
        ],
        doc="User statistics and metadata"
    )
    module.types.append(stats_struct)

    # =========================================================================
    # 2. Enums
    # =========================================================================

    # Simple enum
    status_enum = IREnum(
        name="UserStatus",
        variants=[
            IREnumVariant(name="Active"),
            IREnumVariant(name="Inactive"),
            IREnumVariant(name="Suspended"),
        ],
        doc="User account status"
    )
    module.enums.append(status_enum)

    # Enum with associated data
    event_enum = IREnum(
        name="Event",
        variants=[
            IREnumVariant(name="Login", associated_types=[IRType(name="string")]),
            IREnumVariant(
                name="Update",
                associated_types=[
                    IRType(name="string"),
                    IRType(name="int")
                ]
            ),
            IREnumVariant(name="Logout"),
        ],
        doc="User events"
    )
    module.enums.append(event_enum)

    # =========================================================================
    # 3. Functions
    # =========================================================================

    # Simple function
    greet_func = IRFunction(
        name="greet_user",
        params=[IRParameter(name="username", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[
            IRReturn(
                value=IRCall(
                    function=IRIdentifier(name="format"),
                    args=[
                        IRLiteral(value="Hello, {}!", literal_type=LiteralType.STRING),
                        IRIdentifier(name="username")
                    ]
                )
            )
        ],
        doc="Greet a user by username"
    )
    module.functions.append(greet_func)

    # Function with error handling
    validate_func = IRFunction(
        name="validate_age",
        params=[IRParameter(name="age", param_type=IRType(name="int"))],
        return_type=IRType(name="null"),
        throws=["ValidationError"],
        body=[
            IRIf(
                condition=IRBinaryOp(
                    op=BinaryOperator.LESS_THAN,
                    left=IRIdentifier(name="age"),
                    right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                ),
                then_body=[
                    IRReturn(
                        value=IRCall(
                            function=IRIdentifier(name="Err"),
                            args=[
                                IRCall(
                                    function=IRIdentifier(name="ValidationError"),
                                    args=[
                                        IRLiteral(
                                            value="Age cannot be negative",
                                            literal_type=LiteralType.STRING
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ],
                else_body=[]
            ),
            IRReturn(
                value=IRCall(
                    function=IRIdentifier(name="Ok"),
                    args=[IRLiteral(value=None, literal_type=LiteralType.NULL)]
                )
            )
        ],
        doc="Validate user age"
    )
    module.functions.append(validate_func)

    # Async function
    fetch_func = IRFunction(
        name="fetch_user",
        params=[IRParameter(name="id", param_type=IRType(name="string"))],
        return_type=IRType(name="User", is_optional=True),
        is_async=True,
        body=[
            IRReturn(
                value=IRCall(
                    function=IRIdentifier(name="database_query"),
                    args=[IRIdentifier(name="id")]
                )
            )
        ],
        doc="Asynchronously fetch user from database"
    )
    module.functions.append(fetch_func)

    # Function with collections
    filter_func = IRFunction(
        name="filter_active_users",
        params=[
            IRParameter(
                name="users",
                param_type=IRType(
                    name="array",
                    generic_args=[IRType(name="User")]
                )
            )
        ],
        return_type=IRType(
            name="array",
            generic_args=[IRType(name="User")]
        ),
        body=[
            IRAssignment(
                target="result",
                value=IRArray(elements=[]),
                is_declaration=True
            ),
            IRFor(
                iterator="user",
                iterable=IRIdentifier(name="users"),
                body=[
                    IRIf(
                        condition=IRIdentifier(name="user_active"),
                        then_body=[
                            IRCall(
                                function=IRPropertyAccess(
                                    object=IRIdentifier(name="result"),
                                    property="push"
                                ),
                                args=[IRIdentifier(name="user")]
                            )
                        ],
                        else_body=[]
                    )
                ]
            ),
            IRReturn(value=IRIdentifier(name="result"))
        ],
        doc="Filter users to only active ones"
    )
    module.functions.append(filter_func)

    # =========================================================================
    # 4. Impl Block (Methods)
    # =========================================================================

    user_impl = IRClass(
        name="User",
        constructor=IRFunction(
            name="new",
            params=[
                IRParameter(name="id", param_type=IRType(name="string")),
                IRParameter(name="username", param_type=IRType(name="string")),
                IRParameter(name="age", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="User"),
            body=[]  # Generator will create struct initialization
        ),
        methods=[
            IRFunction(
                name="is_adult",
                params=[],
                return_type=IRType(name="bool"),
                body=[
                    IRReturn(
                        value=IRBinaryOp(
                            op=BinaryOperator.GREATER_EQUAL,
                            left=IRPropertyAccess(
                                object=IRIdentifier(name="self"),
                                property="age"
                            ),
                            right=IRLiteral(value=18, literal_type=LiteralType.INTEGER)
                        )
                    )
                ],
                doc="Check if user is an adult"
            ),
            IRFunction(
                name="update_username",
                params=[
                    IRParameter(name="new_username", param_type=IRType(name="string"))
                ],
                return_type=IRType(name="null"),
                body=[
                    IRAssignment(
                        target="self.username",
                        value=IRIdentifier(name="new_username"),
                        is_declaration=False
                    )
                ],
                doc="Update the username"
            )
        ]
    )
    module.classes.append(user_impl)

    # =========================================================================
    # 5. Trait Definition
    # =========================================================================

    drawable_trait = IRClass(
        name="Validator",
        methods=[
            IRFunction(
                name="validate",
                params=[],
                return_type=IRType(name="bool"),
                body=[],
                doc="Validate the object"
            )
        ],
        doc="Trait for validatable objects"
    )
    drawable_trait.metadata['rust_trait'] = True
    module.classes.append(drawable_trait)

    return module


def main():
    """Generate and display comprehensive Rust code."""
    print("=" * 70)
    print("Rust Generator V2 - Comprehensive Demo")
    print("=" * 70)
    print()

    # Create comprehensive module
    module = create_comprehensive_module()

    # Generate Rust code
    rust_code = generate_rust(module)

    # Display results
    print("Generated Rust Code:")
    print("=" * 70)
    print(rust_code)
    print("=" * 70)

    # Show statistics
    print()
    print("Statistics:")
    print("-" * 70)
    print(f"  Structs:      {len(module.types)}")
    print(f"  Enums:        {len(module.enums)}")
    print(f"  Functions:    {len(module.functions)}")
    print(f"  Classes/Impls: {len(module.classes)}")
    print(f"  Lines of code: {len(rust_code.splitlines())}")
    print(f"  Characters:    {len(rust_code)}")
    print("=" * 70)

    # Save to file
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/generated_example.rs"
    with open(output_file, 'w') as f:
        f.write(rust_code)
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
