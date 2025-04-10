from collections.abc import Iterable, Iterator
import enum
from typing import overload

import _pymimir


class BooleanConstructor:
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def evaluate(self, evaluation_context: "mimir::languages::dl::EvaluationContext") -> "mimir::languages::dl::DenotationImpl<mimir::languages::dl::BooleanTag>": ...

    def accept(self, visitor: ConstructorVisitor) -> None: ...

    def get_index(self) -> int: ...

class BooleanConstructorList:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: BooleanConstructorList) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[BooleanConstructor], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[BooleanConstructor]: ...

    @overload
    def __getitem__(self, arg: int, /) -> BooleanConstructor: ...

    @overload
    def __getitem__(self, arg: slice, /) -> BooleanConstructorList: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: BooleanConstructor, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: BooleanConstructor, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> BooleanConstructor:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: BooleanConstructorList, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: BooleanConstructor, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: BooleanConstructorList, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    @overload
    def __contains__(self, arg: BooleanConstructor, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: BooleanConstructor, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: BooleanConstructor, /) -> None:
        """Remove first occurrence of `arg`."""

class CNFGrammar:
    def __init__(self, bnf_description: str, domain: _pymimir.advanced.formalism.Domain) -> None: ...

    @staticmethod
    def create(type: GrammarSpecificationEnum, domain: _pymimir.advanced.formalism.Domain) -> CNFGrammar: ...

    def accept(self, visitor: "mimir::languages::dl::cnf_grammar::IVisitor") -> None: ...

    @overload
    def test_match(self, arg: NumericalConstructor, /) -> bool: ...

    @overload
    def test_match(self, arg: RoleConstructor, /) -> bool: ...

    @overload
    def test_match(self, arg: BooleanConstructor, /) -> bool: ...

    @overload
    def test_match(self, arg: NumericalConstructor, /) -> bool: ...

    def get_repositories(self) -> "mimir::languages::dl::cnf_grammar::Repositories": ...

    def get_domain(self) -> _pymimir.advanced.formalism.Domain: ...

class ConceptBotConstructor(ConceptConstructor):
    pass

class ConceptConstructor:
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def evaluate(self, evaluation_context: "mimir::languages::dl::EvaluationContext") -> "mimir::languages::dl::DenotationImpl<mimir::languages::dl::ConceptTag>": ...

    def accept(self, visitor: ConstructorVisitor) -> None: ...

    def get_index(self) -> int: ...

class ConceptConstructorList:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: ConceptConstructorList) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[ConceptConstructor], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[ConceptConstructor]: ...

    @overload
    def __getitem__(self, arg: int, /) -> ConceptConstructor: ...

    @overload
    def __getitem__(self, arg: slice, /) -> ConceptConstructorList: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: ConceptConstructor, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: ConceptConstructor, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> ConceptConstructor:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: ConceptConstructorList, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: ConceptConstructor, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: ConceptConstructorList, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    @overload
    def __contains__(self, arg: ConceptConstructor, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: ConceptConstructor, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: ConceptConstructor, /) -> None:
        """Remove first occurrence of `arg`."""

class ConceptTopConstructor(ConceptConstructor):
    pass

class ConstructorVisitor:
    def __init__(self) -> None: ...

    @overload
    def visit(self, arg: ConceptBotConstructor, /) -> None: ...

    @overload
    def visit(self, arg: ConceptTopConstructor, /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicStateImpl<mimir::formalism::StaticTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicStateImpl<mimir::formalism::FluentTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicStateImpl<mimir::formalism::DerivedTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicGoalImpl<mimir::formalism::StaticTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicGoalImpl<mimir::formalism::FluentTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptAtomicGoalImpl<mimir::formalism::DerivedTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptIntersectionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptUnionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptNegationImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptValueRestrictionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptExistentialQuantificationImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptRoleValueMapContainmentImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptRoleValueMapEqualityImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::ConceptNominalImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleUniversalImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicStateImpl<mimir::formalism::StaticTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicStateImpl<mimir::formalism::FluentTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicStateImpl<mimir::formalism::DerivedTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicGoalImpl<mimir::formalism::StaticTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicGoalImpl<mimir::formalism::FluentTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleAtomicGoalImpl<mimir::formalism::DerivedTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleIntersectionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleUnionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleComplementImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleInverseImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleCompositionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleTransitiveClosureImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleReflexiveTransitiveClosureImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleRestrictionImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::RoleIdentityImpl", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::BooleanAtomicStateImpl<mimir::formalism::StaticTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::BooleanAtomicStateImpl<mimir::formalism::FluentTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::BooleanAtomicStateImpl<mimir::formalism::DerivedTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::BooleanNonemptyImpl<mimir::languages::dl::ConceptTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::BooleanNonemptyImpl<mimir::languages::dl::RoleTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::NumericalCountImpl<mimir::languages::dl::ConceptTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::NumericalCountImpl<mimir::languages::dl::RoleTag>", /) -> None: ...

    @overload
    def visit(self, arg: "mimir::languages::dl::NumericalDistanceImpl", /) -> None: ...

class GrammarSpecificationEnum(enum.Enum):
    FRANCES_ET_AL_AAAI2021 = 0

class NumericalConstructor:
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def evaluate(self, evaluation_context: "mimir::languages::dl::EvaluationContext") -> "mimir::languages::dl::DenotationImpl<mimir::languages::dl::NumericalTag>": ...

    def accept(self, visitor: ConstructorVisitor) -> None: ...

    def get_index(self) -> int: ...

class NumericalConstructorList:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: NumericalConstructorList) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[NumericalConstructor], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[NumericalConstructor]: ...

    @overload
    def __getitem__(self, arg: int, /) -> NumericalConstructor: ...

    @overload
    def __getitem__(self, arg: slice, /) -> NumericalConstructorList: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: NumericalConstructor, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: NumericalConstructor, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> NumericalConstructor:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: NumericalConstructorList, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: NumericalConstructor, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: NumericalConstructorList, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    @overload
    def __contains__(self, arg: NumericalConstructor, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: NumericalConstructor, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: NumericalConstructor, /) -> None:
        """Remove first occurrence of `arg`."""

class Repositories:
    def __init__(self) -> None: ...

    def get_or_create_concept(self, sentence: str, domain: _pymimir.advanced.formalism.Domain) -> ConceptConstructor: ...

    def get_or_create_role(self, sentence: str, domain: _pymimir.advanced.formalism.Domain) -> RoleConstructor: ...

    def get_or_create_boolean(self, sentence: str, domain: _pymimir.advanced.formalism.Domain) -> BooleanConstructor: ...

    def get_or_create_numerical(self, sentence: str, domain: _pymimir.advanced.formalism.Domain) -> NumericalConstructor: ...

    def get_or_create_concept_bot(self) -> ConceptConstructor: ...

    def get_or_create_concept_top(self) -> ConceptConstructor: ...

    def get_or_create_concept_intersection(self, left_concept: ConceptConstructor, right_concept: ConceptConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_union(self, left_concept: ConceptConstructor, right_concept: ConceptConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_negation(self, concept_: ConceptConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_value_restriction(self, role: RoleConstructor, concept_: ConceptConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_existential_quantification(self, role: RoleConstructor, concept_: ConceptConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_role_value_map_containment(self, left_role: RoleConstructor, right_role: RoleConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_role_value_map_equality(self, left_role: RoleConstructor, right_role: RoleConstructor) -> ConceptConstructor: ...

    def get_or_create_concept_nominal(self, object: _pymimir.advanced.formalism.Object) -> ConceptConstructor: ...

    def get_or_create_role_universal(self) -> RoleConstructor: ...

    def get_or_create_role_intersection(self, left_role: RoleConstructor, right_role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_union(self, left_role: RoleConstructor, right_role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_complement(self, role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_inverse(self, role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_composition(self, left_role: RoleConstructor, right_role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_transitive_closure(self, role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_reflexive_transitive_closure(self, role: RoleConstructor) -> RoleConstructor: ...

    def get_or_create_role_restriction(self, role: RoleConstructor, concept_: ConceptConstructor) -> RoleConstructor: ...

    def get_or_create_role_identity(self, concept_: ConceptConstructor) -> RoleConstructor: ...

    def get_or_create_concept_atomic_state_static(self, predicate: _pymimir.advanced.formalism.StaticPredicate) -> ConceptConstructor: ...

    def get_or_create_concept_atomic_state_fluent(self, predicate: _pymimir.advanced.formalism.FluentPredicate) -> ConceptConstructor: ...

    def get_or_create_concept_atomic_state_derived(self, predicate: _pymimir.advanced.formalism.DerivedPredicate) -> ConceptConstructor: ...

    def get_or_create_concept_atomic_goal_static(self, predicate: _pymimir.advanced.formalism.StaticPredicate, polarity: bool) -> ConceptConstructor: ...

    def get_or_create_concept_atomic_goal_fluent(self, predicate: _pymimir.advanced.formalism.FluentPredicate, polarity: bool) -> ConceptConstructor: ...

    def get_or_create_concept_atomic_goal_derived(self, predicate: _pymimir.advanced.formalism.DerivedPredicate, polarity: bool) -> ConceptConstructor: ...

    def get_or_create_role_atomic_state_static(self, predicate: _pymimir.advanced.formalism.StaticPredicate) -> RoleConstructor: ...

    def get_or_create_role_atomic_state_fluent(self, predicate: _pymimir.advanced.formalism.FluentPredicate) -> RoleConstructor: ...

    def get_or_create_role_atomic_state_derived(self, predicate: _pymimir.advanced.formalism.DerivedPredicate) -> RoleConstructor: ...

    def get_or_create_role_atomic_goal_static(self, predicate: _pymimir.advanced.formalism.StaticPredicate, polarity: bool) -> RoleConstructor: ...

    def get_or_create_role_atomic_goal_fluent(self, predicate: _pymimir.advanced.formalism.FluentPredicate, polarity: bool) -> RoleConstructor: ...

    def get_or_create_role_atomic_goal_derived(self, predicate: _pymimir.advanced.formalism.DerivedPredicate, polarity: bool) -> RoleConstructor: ...

    def get_or_create_boolean_atomic_state_static(self, predicate: _pymimir.advanced.formalism.StaticPredicate) -> BooleanConstructor: ...

    def get_or_create_boolean_atomic_state_fluent(self, predicate: _pymimir.advanced.formalism.FluentPredicate) -> BooleanConstructor: ...

    def get_or_create_boolean_atomic_state_derived(self, predicate: _pymimir.advanced.formalism.DerivedPredicate) -> BooleanConstructor: ...

    def get_or_create_boolean_nonempty_concept(self, constructor: ConceptConstructor) -> BooleanConstructor: ...

    def get_or_create_boolean_nonempty_role(self, constructor: RoleConstructor) -> BooleanConstructor: ...

    def get_or_create_numerical_count_concept(self, constructor: ConceptConstructor) -> NumericalConstructor: ...

    def get_or_create_numerical_count_role(self, constructor: RoleConstructor) -> NumericalConstructor: ...

    def get_or_create_numerical_distance(self, left_concept: ConceptConstructor, role: RoleConstructor, right_concept: ConceptConstructor) -> NumericalConstructor: ...

class RoleConstructor:
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def evaluate(self, evaluation_context: "mimir::languages::dl::EvaluationContext") -> "mimir::languages::dl::DenotationImpl<mimir::languages::dl::RoleTag>": ...

    def accept(self, visitor: ConstructorVisitor) -> None: ...

    def get_index(self) -> int: ...

class RoleConstructorList:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: RoleConstructorList) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[RoleConstructor], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[RoleConstructor]: ...

    @overload
    def __getitem__(self, arg: int, /) -> RoleConstructor: ...

    @overload
    def __getitem__(self, arg: slice, /) -> RoleConstructorList: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: RoleConstructor, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: RoleConstructor, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> RoleConstructor:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: RoleConstructorList, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: RoleConstructor, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: RoleConstructorList, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    @overload
    def __contains__(self, arg: RoleConstructor, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: RoleConstructor, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: RoleConstructor, /) -> None:
        """Remove first occurrence of `arg`."""
