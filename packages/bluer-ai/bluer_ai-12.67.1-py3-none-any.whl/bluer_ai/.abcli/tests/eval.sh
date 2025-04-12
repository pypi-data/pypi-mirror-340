#! /usr/bin/env bash

function test_bluer_ai_eval() {
    bluer_ai_eval - ls
    abcli_assert "$?" 0

    bluer_ai_eval - lsz
    abcli_assert "$?" 0 not
}
