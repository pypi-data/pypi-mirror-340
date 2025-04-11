#include "bindings.hpp"

#include "../init_declarations.hpp"

using namespace mimir;
using namespace mimir::datasets;
using namespace mimir::formalism;

namespace mimir::bindings
{

void bind_datasets(nb::module_& m)
{
    bind_vertex<graphs::ProblemVertex>(m, PyVertexProperties<graphs::ProblemVertex>::name);
    bind_vertex<graphs::ClassVertex>(m, PyVertexProperties<graphs::ClassVertex>::name);
    bind_edge<graphs::ProblemEdge>(m, PyEdgeProperties<graphs::ProblemEdge>::name);
    bind_edge<graphs::ClassEdge>(m, PyEdgeProperties<graphs::ClassEdge>::name);
    bind_static_graph<graphs::ProblemVertex, graphs::ProblemEdge>(m, "ProblemStaticGraph");
    bind_static_graph<graphs::ClassVertex, graphs::ClassEdge>(m, "ClassStaticGraph");

    nb::class_<StateSpaceImpl::Options>(m, "StateSpaceOptions")
        .def(nb::init<>())
        .def_rw("sort_ascending_by_num_states", &StateSpaceImpl::Options::sort_ascending_by_num_states)
        .def_rw("symmetry_pruning", &StateSpaceImpl::Options::symmetry_pruning)
        .def_rw("remove_if_unsolvable", &StateSpaceImpl::Options::remove_if_unsolvable)
        .def_rw("max_num_states", &StateSpaceImpl::Options::max_num_states)
        .def_rw("timeout_ms", &StateSpaceImpl::Options::timeout_ms);

    nb::class_<TupleGraphImpl::Options>(m, "TupleGraphOptions")
        .def(nb::init<>())
        .def(nb::init<size_t, bool>(), nb::arg("width"), nb::arg("enable_dominance_pruning"))
        .def_rw("width", &TupleGraphImpl::Options::width)
        .def_rw("enable_dominance_pruning", &TupleGraphImpl::Options::enable_dominance_pruning);

    nb::class_<GeneralizedStateSpaceImpl::Options>(m, "GeneralizedStateSpaceOptions")
        .def(nb::init<>())
        .def_rw("symmetry_pruning", &GeneralizedStateSpaceImpl::Options::symmetry_pruning);

    nb::class_<KnowledgeBaseImpl::Options>(m, "KnowledgeBaseOptions")
        .def(nb::init<>())
        .def(nb::init<const state_space::Options&, const GeneralizedStateSpaceImpl::Options&, const std::optional<TupleGraphImpl::Options>&>(),
             nb::arg("state_space_options"),
             nb::arg("generalized_state_space_options"),
             nb::arg("tuple_graph_options") = std::nullopt)
        .def_rw("state_space_options", &KnowledgeBaseImpl::Options::state_space_options)
        .def_rw("generalized_state_space_options", &KnowledgeBaseImpl::Options::generalized_state_space_options)
        .def_rw("tuple_graph_options", &KnowledgeBaseImpl::Options::tuple_graph_options);

    nb::class_<StateSpaceImpl>(m, "StateSpace")
        .def_static(
            "create",
            [](search::SearchContext context, const StateSpaceImpl::Options& options) -> std::optional<StateSpace>
            { return StateSpaceImpl::create(context, options); },
            "context"_a,
            "options"_a = StateSpaceImpl::Options())
        .def_static(
            "create",
            [](search::GeneralizedSearchContext contexts, const StateSpaceImpl::Options& options) -> StateSpaceList
            { return StateSpaceImpl::create(contexts, options); },
            "contexts"_a,
            "options"_a = StateSpaceImpl::Options())
        .def("get_search_context", &StateSpaceImpl::get_search_context, nb::rv_policy::copy)
        .def("get_graph", &StateSpaceImpl::get_graph, nb::rv_policy::reference_internal)
        .def("get_initial_vertex", &StateSpaceImpl::get_initial_vertex, nb::rv_policy::copy)
        .def("get_goal_vertices", &StateSpaceImpl::get_goal_vertices, nb::rv_policy::copy)
        .def("get_unsolvable_vertices", &StateSpaceImpl::get_unsolvable_vertices, nb::rv_policy::copy);

    nb::class_<GeneralizedStateSpaceImpl>(m, "GeneralizedStateSpace")
        .def_static("create", &GeneralizedStateSpaceImpl::create, "state_spaces"_a, "options"_a = GeneralizedStateSpaceImpl::Options())
        .def("get_state_spaces", &GeneralizedStateSpaceImpl::get_state_spaces, nb::rv_policy::copy)
        .def("get_graph", &GeneralizedStateSpaceImpl::get_graph, nb::rv_policy::reference_internal)
        .def("get_initial_vertices", &GeneralizedStateSpaceImpl::get_initial_vertices, nb::rv_policy::copy)
        .def("get_goal_vertices", &GeneralizedStateSpaceImpl::get_goal_vertices, nb::rv_policy::copy)
        .def("get_unsolvable_vertices", &GeneralizedStateSpaceImpl::get_unsolvable_vertices, nb::rv_policy::copy)
        .def("get_state_space",
             nb::overload_cast<const graphs::ClassVertex&>(&GeneralizedStateSpaceImpl::get_state_space, nb::const_),
             nb::rv_policy::reference_internal)
        .def("get_state_space",
             nb::overload_cast<const graphs::ClassEdge&>(&GeneralizedStateSpaceImpl::get_state_space, nb::const_),
             nb::rv_policy::reference_internal)
        .def("get_problem_vertex", &GeneralizedStateSpaceImpl::get_problem_vertex, nb::rv_policy::reference_internal)
        .def("get_problem_edge", &GeneralizedStateSpaceImpl::get_problem_edge, nb::rv_policy::reference_internal)
        .def("get_class_vertex", &GeneralizedStateSpaceImpl::get_class_vertex, nb::rv_policy::reference_internal)
        .def("get_class_edge", &GeneralizedStateSpaceImpl::get_class_edge, nb::rv_policy::reference_internal)
        .def("create_induced_subgraph_from_class_vertex_indices",
             &GeneralizedStateSpaceImpl::create_induced_subgraph_from_class_vertex_indices,
             nb::rv_policy::take_ownership)
        .def("create_induced_subgraph_from_problem_indices",
             &GeneralizedStateSpaceImpl::create_induced_subgraph_from_problem_indices,
             nb::rv_policy::take_ownership);

    nb::class_<KnowledgeBaseImpl>(m, "KnowledgeBase")
        .def_static("create", &KnowledgeBaseImpl::create, "contexts"_a, "options"_a = KnowledgeBaseImpl::Options())
        .def("get_generalized_state_space", &KnowledgeBaseImpl::get_generalized_state_space, nb::rv_policy::reference_internal);
}

}
