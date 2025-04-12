#! /usr/bin/env bash

function test_bluer_ai_plugin_name_from_repo() {
    local options=$1

    if [[ "$abcli_is_github_workflow" == true ]]; then
        bluer_ai_log_warning "plugins are not present in the github workflow."
        return
    fi

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo awesome-bash-cli) \
        abcli
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo abadpour) \
        abadpour
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo roofai) \
        roofai
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo vancouver-watching) \
        vancouver_watching
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo giza) \
        giza
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo hubble) \
        hubble
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo aiart) \
        aiart
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_plugin_name_from_repo notebooks-and-scripts) \
        notebooks_and_scripts
}

function test_bluer_ai_get_module_name_from_plugin() {
    if [[ "$abcli_is_github_workflow" == true ]]; then
        bluer_ai_log_warning "plugins are not present in the github workflow."
        return
    fi

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin abcli) \
        abcli
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin abadpour) \
        abadpour
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin roofai) \
        roofai
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin vancouver_watching) \
        vancouver_watching
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin giza) \
        gizai
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin hubble) \
        hubblescope
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin aiart) \
        articraft
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_ai_get_module_name_from_plugin notebooks_and_scripts) \
        blueflow
}
