def test_eeg_gate_integration(setup_engine):
    engine = setup_engine
    player_a = OrganismProfile(
        nr3c1_density=0.5,
        coherence_credit=0.85,
        bioelectric=BioelectricState(resting_potential_deviation_mv=1.5, gap_junction_density=0.7),
    )
    player_b = OrganismProfile(
        nr3c1_density=0.52,
        coherence_credit=0.80,
        bioelectric=BioelectricState(resting_potential_deviation_mv=2.5, gap_junction_density=0.65),
    )

    result = process_interaction_node(
        player_a=player_a,
        player_b=player_b,
        external_oxtr_stimulus=0.6,
        engine=engine,
        use_eeg_gate=True,
    )

    assert "phase_locked_scalar" in result
    assert "icoh_mean" in result
    assert "field_phase_locked" in result
    assert result["phase_locked"] == (
        result["phase_locked_scalar"] and result["field_phase_locked"]
    )
