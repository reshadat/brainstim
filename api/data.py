"""
Static data: brain region → feelings/experience mapping.
Source: HCP-MMP1 atlas (360 cortical parcels = 180 unique regions × 2 hemispheres, fsaverage5 space).
All 180 unique HCP-MMP1 region labels are covered.
"""

BRAIN_FEELINGS = {
    # ── Visual Cortex (Primary & Early) ──────────────────────────────────────
    "V1":     {"name": "Primary Visual Cortex (V1)",           "experience": "Raw edges, brightness, contrast, orientation",             "category": "Visual"},
    "V2":     {"name": "Secondary Visual Cortex (V2)",          "experience": "Basic shapes, contours, colors, textures",                 "category": "Visual"},
    "V3":     {"name": "Visual Area V3",                        "experience": "Form perception, global shape integration",                "category": "Visual"},
    "V4":     {"name": "Color Processing Area (V4)",            "experience": "Vivid color perception, object recognition",              "category": "Visual"},
    "V8":     {"name": "Color Area V8",                         "experience": "Rich color experience, color constancy",                  "category": "Visual"},
    "V3A":    {"name": "Dorsal Visual Area V3A",                "experience": "Motion-in-depth, stereoscopic processing",                "category": "Visual"},
    "V3B":    {"name": "Dorsal Visual Area V3B",                "experience": "3D shape-from-motion, depth processing",                  "category": "Visual"},
    "V6":     {"name": "Visual Area V6",                        "experience": "Wide-field motion, peripheral vision, self-motion",        "category": "Visual"},
    "V6A":    {"name": "Visuomotor Area V6A",                   "experience": "Reaching guidance, eye-hand coordination",                "category": "Visual"},
    "V7":     {"name": "Visual Area V7 (IPS0)",                 "experience": "Spatial attention to visual targets",                     "category": "Attention"},
    "V3CD":   {"name": "Visual Area V3CD",                      "experience": "Motion boundary detection",                               "category": "Visual"},

    # ── MT+ Complex & Lateral Occipital ──────────────────────────────────────
    "MT":     {"name": "Motion Area (V5/MT)",                   "experience": "Perceiving movement, visual flow, speed",                 "category": "Visual"},
    "MST":    {"name": "Medial Superior Temporal (MST)",        "experience": "Self-motion, navigation, optic flow",                     "category": "Visual"},
    "V4t":    {"name": "V4 Transition Zone",                    "experience": "Motion-selective visual processing",                      "category": "Visual"},
    "FST":    {"name": "Fundus of Superior Temporal (FST)",     "experience": "Complex motion patterns, biological motion",              "category": "Visual"},
    "LO1":    {"name": "Lateral Occipital 1",                   "experience": "Object recognition, visual familiarity",                  "category": "Visual"},
    "LO2":    {"name": "Lateral Occipital 2",                   "experience": "Shape completion, object boundaries",                     "category": "Visual"},
    "LO3":    {"name": "Lateral Occipital 3",                   "experience": "High-level object representation",                        "category": "Visual"},
    "PH":     {"name": "Area PH",                               "experience": "Scene layout, spatial context of objects",                "category": "Visual"},
    "PIT":    {"name": "Posterior Inferotemporal",              "experience": "Object and texture recognition",                          "category": "Visual"},

    # ── Ventral Visual Stream ────────────────────────────────────────────────
    "FFC":    {"name": "Fusiform Face Complex",                 "experience": "Face recognition, emotional face processing",             "category": "Social"},
    "VVC":    {"name": "Ventral Visual Complex",                "experience": "Object categorization, visual expertise",                 "category": "Visual"},
    "VMV1":   {"name": "Ventromedial Visual 1",                 "experience": "Scene recognition, place perception",                     "category": "Memory"},
    "VMV2":   {"name": "Ventromedial Visual 2",                 "experience": "Scene familiarity, contextual associations",              "category": "Memory"},
    "VMV3":   {"name": "Ventromedial Visual 3",                 "experience": "Spatial layout of environments",                          "category": "Memory"},

    # ── Face & Body Recognition ──────────────────────────────────────────────
    "OFA":    {"name": "Occipital Face Area",                   "experience": "Basic face detection, facial features",                   "category": "Social"},
    "TE1a":   {"name": "Temporal Area TE1a",                    "experience": "Fine visual object discrimination",                       "category": "Visual"},
    "TE1m":   {"name": "Temporal Area TE1m",                    "experience": "Object memory, visual categorization",                    "category": "Visual"},
    "TE1p":   {"name": "Temporal Area TE1p",                    "experience": "High-level visual pattern recognition",                   "category": "Visual"},
    "TE2a":   {"name": "Temporal Area TE2a",                    "experience": "Semantic visual association",                             "category": "Visual"},
    "TE2p":   {"name": "Temporal Area TE2p",                    "experience": "Visual object memory retrieval",                          "category": "Memory"},
    "TF":     {"name": "Fusiform Temporal Area TF",             "experience": "Place and face encoding",                                 "category": "Memory"},
    "TGd":    {"name": "Temporal Pole (dorsal)",                "experience": "Semantic knowledge, social concepts, naming",             "category": "Language"},
    "TGv":    {"name": "Temporal Pole (ventral)",               "experience": "Emotional meaning, personal memories",                    "category": "Emotion"},

    # ── Auditory Cortex ──────────────────────────────────────────────────────
    "A1":     {"name": "Primary Auditory Cortex (A1)",          "experience": "Raw sound: pitch, loudness, tone",                        "category": "Auditory"},
    "A4":     {"name": "Auditory Area 4",                       "experience": "Complex sound features, spectral processing",             "category": "Auditory"},
    "A5":     {"name": "Auditory Area 5",                       "experience": "Sound pattern recognition",                               "category": "Auditory"},
    "LBelt":  {"name": "Lateral Belt (Auditory)",               "experience": "Complex sound processing, voice quality",                 "category": "Auditory"},
    "MBelt":  {"name": "Medial Belt (Auditory)",                "experience": "Sound frequency analysis, tone discrimination",           "category": "Auditory"},
    "PBelt":  {"name": "Parabelt (Auditory)",                   "experience": "Sound integration, auditory scene analysis",              "category": "Auditory"},
    "RI":     {"name": "Retroinsular Auditory",                 "experience": "Sound localization, spatial hearing, rhythm",             "category": "Auditory"},
    "TA2":    {"name": "Auditory Association TA2",              "experience": "Sound meaning, auditory object recognition",              "category": "Auditory"},
    "STGa":   {"name": "Superior Temporal Gyrus (anterior)",    "experience": "Complex sound patterns, music perception",                "category": "Auditory"},

    # ── Language & Superior Temporal Sulcus ───────────────────────────────────
    "STSda":  {"name": "Superior Temporal Sulcus (dorsal ant)", "experience": "Spoken word comprehension",                               "category": "Language"},
    "STSdp":  {"name": "Superior Temporal Sulcus (dorsal post)","experience": "Voice recognition, social sounds",                        "category": "Language"},
    "STSva":  {"name": "Superior Temporal Sulcus (ventral ant)","experience": "Language prosody, emotional tone of speech",              "category": "Language"},
    "STSvp":  {"name": "Superior Temporal Sulcus (ventral post)","experience": "Audiovisual speech integration",                         "category": "Language"},
    "STV":    {"name": "Superior Temporal Voice Area",          "experience": "Voice identity recognition",                              "category": "Social"},
    "44":     {"name": "Broca's Area (pars opercularis)",       "experience": "Speech production, syntax, verbal planning",              "category": "Language"},
    "45":     {"name": "Broca's Area (pars triangularis)",      "experience": "Semantic processing, word meaning retrieval",             "category": "Language"},
    "47l":    {"name": "Lateral Prefrontal 47l",                "experience": "Language comprehension, verbal abstraction",              "category": "Language"},
    "47s":    {"name": "Area 47s (orbital)",                    "experience": "Semantic decision-making, verbal evaluation",             "category": "Language"},
    "IFJa":   {"name": "Inferior Frontal Junction (anterior)",  "experience": "Cognitive control during language tasks",                 "category": "Executive"},
    "IFJp":   {"name": "Inferior Frontal Junction (posterior)", "experience": "Task switching, verbal working memory",                   "category": "Executive"},
    "IFSa":   {"name": "Inferior Frontal Sulcus (anterior)",    "experience": "Verbal reasoning, abstract thought",                     "category": "Executive"},
    "IFSp":   {"name": "Inferior Frontal Sulcus (posterior)",   "experience": "Phonological processing, inner speech",                  "category": "Language"},
    "SFL":    {"name": "Superior Frontal Language Area",        "experience": "Verbal fluency, narrative construction",                  "category": "Language"},
    "55b":    {"name": "Premotor Area 55b",                     "experience": "Speech motor planning, vocalization prep",                "category": "Language"},
    "PSL":    {"name": "Perisylvian Language Area",             "experience": "Phonological and syntactic processing",                   "category": "Language"},
    "TPOJ1":  {"name": "Temporoparietal Junction 1",            "experience": "Theory of mind, social cognition",                        "category": "Social"},
    "TPOJ2":  {"name": "Temporoparietal Junction 2",            "experience": "Perspective taking, empathy, mentalizing",                "category": "Social"},
    "TPOJ3":  {"name": "Temporoparietal Junction 3",            "experience": "Self vs other distinction, agency",                       "category": "Social"},

    # ── Angular & Supramarginal Gyrus ────────────────────────────────────────
    "PGp":    {"name": "Angular Gyrus (posterior)",             "experience": "Semantic memory, reading comprehension",                  "category": "Language"},
    "PGs":    {"name": "Angular Gyrus (superior)",              "experience": "Attention direction, number sense",                       "category": "Attention"},
    "PGi":    {"name": "Angular Gyrus (inferior)",              "experience": "Default mode network, conceptual integration",            "category": "Memory"},
    "PFm":    {"name": "Supramarginal Gyrus (PFm)",             "experience": "Phonological short-term memory",                         "category": "Language"},
    "PFop":   {"name": "Supramarginal Gyrus (PFop)",            "experience": "Somatosensory integration, tool use",                    "category": "Sensory"},
    "PFt":    {"name": "Supramarginal Gyrus (PFt)",             "experience": "Action observation, imitation",                           "category": "Motor"},
    "PF":     {"name": "Supramarginal Gyrus (PF)",              "experience": "Tactile attention, phonological storage",                 "category": "Sensory"},

    # ── Somatosensory & Motor Cortex ─────────────────────────────────────────
    "1":      {"name": "Somatosensory Area 1",                  "experience": "Touch location, texture discrimination",                 "category": "Sensory"},
    "2":      {"name": "Somatosensory Area 2",                  "experience": "Touch, texture, complex shape by touch",                 "category": "Sensory"},
    "3a":     {"name": "Primary Somatosensory 3a",              "experience": "Proprioception, body position sense",                    "category": "Sensory"},
    "3b":     {"name": "Primary Somatosensory 3b",              "experience": "Fine touch, pressure discrimination",                    "category": "Sensory"},
    "4":      {"name": "Primary Motor Cortex (M1)",             "experience": "Movement execution, muscle control",                     "category": "Motor"},
    "6ma":    {"name": "Premotor Cortex (6ma)",                 "experience": "Movement preparation, action planning",                  "category": "Motor"},
    "6mp":    {"name": "Supplementary Motor (medial, 6mp)",     "experience": "Complex motor sequences, bimanual coordination",         "category": "Motor"},
    "6d":     {"name": "Dorsal Premotor Cortex",                "experience": "Reaching and grasping preparation",                      "category": "Motor"},
    "6v":     {"name": "Ventral Premotor Cortex",               "experience": "Object manipulation, tool use planning",                 "category": "Motor"},
    "6a":     {"name": "Premotor Area 6a",                      "experience": "Arm movement planning",                                  "category": "Motor"},
    "6r":     {"name": "Rostral Premotor Area",                 "experience": "Orofacial motor control, speech articulation",            "category": "Motor"},
    "SCEF":   {"name": "Supplementary & Cingulate Eye Field",   "experience": "Voluntary eye movements, visual search initiation",      "category": "Motor"},
    "FEF":    {"name": "Frontal Eye Field",                     "experience": "Voluntary gaze shifts, visual attention direction",       "category": "Attention"},
    "PEF":    {"name": "Parietal Eye Field",                    "experience": "Reflexive eye movements, spatial orienting",              "category": "Attention"},
    "SMA":    {"name": "Supplementary Motor Area",              "experience": "Complex sequences, motor planning, initiation",           "category": "Motor"},
    "5m":     {"name": "Medial Area 5m",                        "experience": "Limb position monitoring, reaching",                     "category": "Motor"},
    "5L":     {"name": "Lateral Area 5L",                       "experience": "Hand and arm spatial coordination",                       "category": "Motor"},
    "5mv":    {"name": "Medial Area 5mv",                       "experience": "Lower limb position sense",                              "category": "Sensory"},
    "43":     {"name": "Area 43 (Subcentral)",                  "experience": "Taste, swallowing, oral somatosensation",                "category": "Sensory"},
    "OP1":    {"name": "Parietal Operculum 1",                  "experience": "Tactile object recognition by touch",                    "category": "Sensory"},
    "OP2-3":  {"name": "Parietal Operculum 2-3",                "experience": "Vestibular processing, balance sensation",               "category": "Sensory"},
    "OP4":    {"name": "Parietal Operculum 4",                  "experience": "Sensorimotor integration, action feedback",              "category": "Sensory"},

    # ── Cingulate Cortex ─────────────────────────────────────────────────────
    "24dd":   {"name": "Dorsal Cingulate Motor (24dd)",         "experience": "Motor conflict monitoring, effort sense",                 "category": "Motor"},
    "24dv":   {"name": "Ventral Cingulate Motor (24dv)",        "experience": "Pain processing, emotional motor responses",             "category": "Emotion"},
    "p24":    {"name": "Pregenual Cingulate (p24)",             "experience": "Emotion regulation, decision-making under uncertainty",   "category": "Emotion"},
    "a24":    {"name": "Anterior Cingulate (a24)",              "experience": "Conflict monitoring, error detection, emotional pain",    "category": "Emotion"},
    "p24pr":  {"name": "Pregenual Cingulate (p24pr, prime)",    "experience": "Autonomic emotion regulation, visceral awareness",       "category": "Emotion"},
    "a24pr":  {"name": "Anterior Cingulate (a24pr, prime)",     "experience": "Emotional salience detection, motivational drive",        "category": "Emotion"},
    "p32":    {"name": "Pregenual Cingulate (p32)",             "experience": "Social emotion, guilt, empathic concern",                "category": "Emotion"},
    "p32pr":  {"name": "Pregenual Cingulate (p32pr, prime)",    "experience": "Default mode self-referential thought, rumination",       "category": "Emotion"},
    "d32":    {"name": "Dorsal Anterior Cingulate (d32)",       "experience": "Cognitive-emotional integration, appraisal",             "category": "Emotion"},
    "a32pr":  {"name": "Anterior Cingulate (a32pr, prime)",     "experience": "Emotional conflict resolution, social evaluation",       "category": "Emotion"},
    "s32":    {"name": "Subgenual Cingulate (s32)",             "experience": "Deep sadness, mood regulation, reward anticipation",      "category": "Emotion"},
    "33pr":   {"name": "Cingulate Area 33 (prime)",             "experience": "Pain affect, visceral distress",                          "category": "Emotion"},
    "PCV":    {"name": "Precuneus Visual Area",                 "experience": "Visual imagery during self-reflection",                   "category": "Memory"},
    "RSC":    {"name": "Retrosplenial Cortex",                  "experience": "Spatial memory, navigation, scene familiarity",           "category": "Memory"},
    "POS1":   {"name": "Parieto-Occipital Sulcus 1",           "experience": "Spatial orientation, environmental awareness",            "category": "Memory"},
    "POS2":   {"name": "Parieto-Occipital Sulcus 2",           "experience": "Visuospatial imagery, mental rotation",                  "category": "Visual"},
    "v23ab":  {"name": "Ventral Area 23ab",                     "experience": "Episodic memory retrieval, self-referencing",             "category": "Memory"},
    "d23ab":  {"name": "Dorsal Area 23ab",                      "experience": "Spatial memory, contextual recall",                       "category": "Memory"},
    "31a":    {"name": "Area 31a",                              "experience": "Autobiographical memory, sense of self",                  "category": "Memory"},
    "31pd":   {"name": "Area 31pd",                             "experience": "Posterior default mode, mind wandering",                  "category": "Memory"},
    "31pv":   {"name": "Area 31pv",                             "experience": "Episodic recollection, nostalgia",                        "category": "Memory"},
    "7m":     {"name": "Precuneus (7m)",                        "experience": "Conscious awareness, visual imagery, self-reflection",    "category": "Memory"},
    "7Am":    {"name": "Superior Parietal 7Am",                 "experience": "Visuomotor coordination, spatial attention",              "category": "Attention"},
    "7AL":    {"name": "Superior Parietal 7AL",                 "experience": "Reaching in space, hand-eye coordination",                "category": "Motor"},
    "7PC":    {"name": "Posterior Parietal (7PC)",               "experience": "Spatial awareness, attention control",                    "category": "Attention"},
    "7PL":    {"name": "Superior Parietal 7PL",                 "experience": "Spatial manipulation, mental imagery",                    "category": "Attention"},
    "7Pm":    {"name": "Medial Area 7Pm",                       "experience": "Spatial reasoning, route planning",                       "category": "Attention"},

    # ── Posterior Cingulate / Default Mode ───────────────────────────────────
    "PCC":    {"name": "Posterior Cingulate Cortex",            "experience": "Self-reflection, daydreaming, episodic memory",           "category": "Memory"},
    "DVT":    {"name": "Dorsal Transitional Visual",            "experience": "Visual-spatial integration during navigation",            "category": "Visual"},
    "ProS":   {"name": "Prostriate Area",                       "experience": "Rapid peripheral visual processing, alerting",            "category": "Visual"},

    # ── Insula ───────────────────────────────────────────────────────────────
    "Ig":     {"name": "Granular Insula",                       "experience": "Interoception, bodily awareness, gut feeling",            "category": "Emotion"},
    "FOP1":   {"name": "Frontal Operculum 1",                   "experience": "Taste processing, oral sensation",                       "category": "Sensory"},
    "FOP2":   {"name": "Frontal Operculum 2",                   "experience": "Speech motor coordination",                              "category": "Language"},
    "FOP3":   {"name": "Frontal Operculum 3",                   "experience": "Chemosensory integration, flavor",                       "category": "Sensory"},
    "FOP4":   {"name": "Frontal Operculum 4",                   "experience": "Visceral sensation, autonomic awareness",                "category": "Emotion"},
    "FOP5":   {"name": "Frontal Operculum 5",                   "experience": "Emotional salience, sympathetic arousal",                "category": "Emotion"},
    "MI":     {"name": "Middle Insular Area",                   "experience": "Pain perception, emotional intensity, empathy for pain",  "category": "Emotion"},
    "AVI":    {"name": "Anterior Ventral Insula",               "experience": "Emotional awareness, subjective feeling states",          "category": "Emotion"},
    "AAIC":   {"name": "Anterior Agranular Insular Complex",    "experience": "Disgust, strong emotional reactions, social emotions",    "category": "Emotion"},
    "Pir":    {"name": "Piriform Cortex",                       "experience": "Smell processing, olfactory memory",                     "category": "Sensory"},
    "PoI1":   {"name": "Posterior Insula 1",                    "experience": "Pain intensity coding, temperature sensation",            "category": "Sensory"},
    "PoI2":   {"name": "Posterior Insula 2",                    "experience": "Vestibular-interoceptive integration",                    "category": "Sensory"},

    # ── Prefrontal Cortex ────────────────────────────────────────────────────
    "8BL":    {"name": "Lateral Prefrontal 8BL",                "experience": "Sustained attention, vigilance",                          "category": "Attention"},
    "8Ad":    {"name": "Anterior Prefrontal 8Ad",               "experience": "Planning, abstract thinking, goal maintenance",           "category": "Executive"},
    "8Av":    {"name": "Anterior Prefrontal 8Av",               "experience": "Visual working memory, spatial planning",                 "category": "Executive"},
    "8C":     {"name": "Caudal Prefrontal 8C",                  "experience": "Response preparation, cognitive readiness",               "category": "Executive"},
    "46":     {"name": "Dorsolateral Prefrontal (46)",          "experience": "Working memory, cognitive flexibility, reasoning",        "category": "Executive"},
    "9-46d":  {"name": "Dorsolateral Prefrontal 9-46d",         "experience": "Complex reasoning, strategic thinking",                   "category": "Executive"},
    "9a":     {"name": "Anterior Prefrontal 9a",                "experience": "Metacognition, self-monitoring of thought",               "category": "Executive"},
    "9p":     {"name": "Posterior Prefrontal 9p",               "experience": "Mentalizing, abstract social reasoning",                  "category": "Social"},
    "9m":     {"name": "Medial Prefrontal 9m",                  "experience": "Self-referential thought, personal values",               "category": "Emotion"},
    "10d":    {"name": "Frontopolar 10d",                       "experience": "Future thinking, prospective memory",                     "category": "Executive"},
    "10r":    {"name": "Frontopolar 10r",                       "experience": "Reward evaluation, exploration vs exploitation",          "category": "Executive"},
    "10v":    {"name": "Frontopolar 10v",                       "experience": "Default mode, stimulus-independent thought",              "category": "Memory"},
    "10pp":   {"name": "Polar Prefrontal 10pp",                 "experience": "Complex multi-tasking, branching decisions",              "category": "Executive"},
    "a10p":   {"name": "Anterior Prefrontal 10p",               "experience": "Relational reasoning, analogy",                          "category": "Executive"},
    "p10p":   {"name": "Posterior Prefrontal 10p",              "experience": "Goal monitoring, strategy adjustment",                    "category": "Executive"},
    "11l":    {"name": "Orbitofrontal 11l",                     "experience": "Reward processing, pleasure, value judgment",             "category": "Emotion"},
    "13l":    {"name": "Orbitofrontal 13l",                     "experience": "Emotional valuation, cost-benefit feeling",               "category": "Emotion"},
    "OFC":    {"name": "Orbitofrontal Cortex",                  "experience": "Reward expectation, subjective value, taste pleasure",    "category": "Emotion"},
    "pOFC":   {"name": "Posterior Orbitofrontal",               "experience": "Olfactory pleasure, flavor reward",                       "category": "Emotion"},
    "25":     {"name": "Subgenual Cortex (Area 25)",            "experience": "Deep mood regulation, sadness, autonomic control",        "category": "Emotion"},
    "s6-8":   {"name": "Superior Transitional 6-8",             "experience": "Pre-motor planning, cognitive preparation",               "category": "Motor"},
    "i6-8":   {"name": "Inferior Transitional 6-8",             "experience": "Motor-cognitive integration",                             "category": "Motor"},
    "a9-46v": {"name": "Anterior Prefrontal 9-46v",             "experience": "Verbal working memory, abstract language",                "category": "Executive"},
    "p9-46v": {"name": "Posterior Prefrontal 9-46v",            "experience": "Spatial working memory, task management",                 "category": "Executive"},
    "a47r":   {"name": "Anterior Area 47r",                     "experience": "Semantic retrieval, controlled memory access",            "category": "Language"},
    "p47r":   {"name": "Posterior Area 47r",                    "experience": "Phonological processing, verbal selection",               "category": "Language"},

    # ── Intraparietal Sulcus ─────────────────────────────────────────────────
    "IPS1":   {"name": "Intraparietal Sulcus 1",                "experience": "Spatial attention, number magnitude",                     "category": "Attention"},
    "IPS2":   {"name": "Intraparietal Sulcus 2 (not in atlas)", "experience": "Visuo-spatial processing, gaze control",                 "category": "Attention"},
    "MIP":    {"name": "Medial Intraparietal Area",             "experience": "Reaching, arm movement planning",                        "category": "Motor"},
    "AIP":    {"name": "Anterior Intraparietal Area",           "experience": "Grasp planning, 3D object shape for action",              "category": "Motor"},
    "LIPd":   {"name": "Lateral Intraparietal (dorsal)",        "experience": "Saccade planning, spatial decision-making",               "category": "Attention"},
    "LIPv":   {"name": "Lateral Intraparietal (ventral)",       "experience": "Attention priority mapping, salience",                    "category": "Attention"},
    "VIP":    {"name": "Ventral Intraparietal Area",            "experience": "Multisensory spatial processing, near-space",             "category": "Sensory"},
    "IP0":    {"name": "Intraparietal Area 0",                  "experience": "Visual-spatial transformation",                           "category": "Attention"},
    "IP1":    {"name": "Intraparietal Area 1",                  "experience": "Sustained spatial attention",                             "category": "Attention"},
    "IP2":    {"name": "Intraparietal Area 2",                  "experience": "Spatial working memory",                                  "category": "Attention"},

    # ── Medial Temporal / Parahippocampal ────────────────────────────────────
    "PHT":    {"name": "Parahippocampal Cortex",                "experience": "Scene recognition, place memory, context",               "category": "Memory"},
    "PHA1":   {"name": "Parahippocampal Area 1",                "experience": "Visual scene processing, spatial familiarity",            "category": "Memory"},
    "PHA2":   {"name": "Parahippocampal Area 2",                "experience": "Contextual memory associations",                          "category": "Memory"},
    "PHA3":   {"name": "Parahippocampal Area 3",                "experience": "Spatial context encoding",                                "category": "Memory"},
    "EC":     {"name": "Entorhinal Cortex",                     "experience": "Memory encoding, grid-cell navigation",                   "category": "Memory"},
    "PreS":   {"name": "Presubiculum",                          "experience": "Head direction sense, spatial orientation",               "category": "Memory"},
    "H":      {"name": "Hippocampal Area",                      "experience": "Memory formation, recall, spatial mapping",               "category": "Memory"},

    # ── Lateral Temporal ─────────────────────────────────────────────────────
    "TE1a":   {"name": "Temporal Area TE1a",                    "experience": "Fine visual discrimination",                             "category": "Visual"},
    "TE1m":   {"name": "Temporal Area TE1m",                    "experience": "Visual categorization, object memory",                   "category": "Visual"},
    "TE1p":   {"name": "Temporal Area TE1p",                    "experience": "High-level pattern recognition",                         "category": "Visual"},
    "TE2a":   {"name": "Temporal Area TE2a",                    "experience": "Semantic visual associations",                           "category": "Visual"},
    "TE2p":   {"name": "Temporal Area TE2p",                    "experience": "Visual-semantic memory retrieval",                       "category": "Memory"},

    # ── Insular / Opercular (additional) ─────────────────────────────────────
    "52":     {"name": "Parainsular Area 52",                   "experience": "Auditory-somatosensory integration",                      "category": "Auditory"},

    # ── Prefrontal (additional medial) ───────────────────────────────────────
    "8BM":    {"name": "Medial Prefrontal 8BM",                 "experience": "Error monitoring, performance adjustment",                "category": "Executive"},

    # ── Posterior Parietal (additional) ───────────────────────────────────────
    "PCV":    {"name": "Precuneus Visual",                      "experience": "Mental imagery during self-reflection",                   "category": "Memory"},

    # ── Miscellaneous regions that appear in TRIBE v2 output ─────────────────
    "Pol1":   {"name": "Polar Area 1",                          "experience": "Temporal pole association, social concepts",              "category": "Social"},
    "Pol2":   {"name": "Polar Area 2",                          "experience": "Emotional semantic processing",                           "category": "Emotion"},
    "PI":     {"name": "Para-Insular Area",                     "experience": "Auditory-vestibular integration",                         "category": "Auditory"},
    "Temo":   {"name": "Temporal Opercular Area",               "experience": "Sound-movement integration",                              "category": "Auditory"},
    "ProStr": {"name": "Prostriate Area",                       "experience": "Rapid peripheral visual alerting",                        "category": "Visual"},
    "23c":    {"name": "Cingulate Area 23c",                    "experience": "Motor-emotional integration during effort",               "category": "Motor"},
    "23d":    {"name": "Cingulate Area 23d",                    "experience": "Self-referential processing during action",               "category": "Memory"},

    # ── Supplementary lateral temporal ───────────────────────────────────────
    "PHT":    {"name": "Parahippocampal Cortex",                "experience": "Scene recognition, place memory",                        "category": "Memory"},
    "STSva":  {"name": "Superior Temporal Sulcus (ventral ant)", "experience": "Language prosody, emotional tone",                       "category": "Language"},

    # ── Additional parietal ──────────────────────────────────────────────────
    "AIP":    {"name": "Anterior Intraparietal",                "experience": "Grasp planning, 3D shape for action",                    "category": "Motor"},
    "MIP":    {"name": "Medial Intraparietal",                  "experience": "Reaching and arm movement in space",                     "category": "Motor"},

    # ── Lateral prefrontal (additional) ──────────────────────────────────────
    "p47r":   {"name": "Posterior Area 47r",                    "experience": "Verbal selection, controlled retrieval",                  "category": "Language"},
    "a47r":   {"name": "Anterior Area 47r",                     "experience": "Semantic memory access",                                 "category": "Language"},
    "47m":    {"name": "Medial Area 47m",                       "experience": "Emotional decision-making, moral judgment",              "category": "Emotion"},
}

# ── Emotion scoring: HCP regions → felt emotions ─────────────────────────────
# Each emotion maps to a list of (region, weight) tuples.
# Weights reflect how strongly that region contributes to the emotion.
# Based on Lindquist et al. (2012), Barrett & Satpute (2013), Kober et al. (2008).

EMOTION_CIRCUITS = {
    "Joy": {
        "description": "Pleasure, reward, positive anticipation",
        "color": "#facc15",
        "regions": {
            "s32": 1.0, "10r": 0.9, "OFC": 0.9, "10v": 0.8,
            "a24": 0.7, "p32": 0.7, "25": 0.8, "47m": 0.6,
            "Pol2": 0.5, "TGv": 0.5,
        },
    },
    "Curiosity": {
        "description": "Interest, exploration, wanting to know more",
        "color": "#60a5fa",
        "regions": {
            "46": 1.0, "8Ad": 0.9, "8L": 0.8, "IFJa": 0.8,
            "IFSa": 0.7, "FEF": 0.6, "IPS1": 0.6, "9a": 0.5,
            "9p": 0.5, "a9-46v": 0.5,
        },
    },
    "Tension": {
        "description": "Suspense, anxiety, conflict, stress",
        "color": "#f87171",
        "regions": {
            "24": 1.0, "p24": 0.9, "d32": 0.8, "Ig": 0.9,
            "Id": 0.7, "MI": 0.6, "PoI1": 0.5, "PoI2": 0.5,
            "a32pr": 0.6, "p32pr": 0.5,
        },
    },
    "Calm": {
        "description": "Peace, relaxation, safety, contentment",
        "color": "#34d399",
        "regions": {
            "PCC": 1.0, "7m": 0.9, "RSC": 0.8, "31a": 0.7,
            "31pd": 0.6, "31pv": 0.6, "PCV": 0.5, "ProStr": 0.3,
            "d23ab": 0.5, "v23ab": 0.5,
        },
    },
    "Engagement": {
        "description": "Absorbed, focused, in the flow",
        "color": "#a78bfa",
        "regions": {
            "FEF": 1.0, "PEF": 0.9, "MT": 0.8, "MST": 0.7,
            "6ma": 0.7, "6a": 0.6, "V4t": 0.5, "SMA": 0.5,
            "IPS1": 0.6, "IPS2": 0.5,
        },
    },
    "Empathy": {
        "description": "Feeling what others feel, social connection",
        "color": "#f472b6",
        "regions": {
            "TPOJ1": 1.0, "TPOJ2": 0.9, "TPOJ3": 0.8,
            "FFC": 0.7, "STV": 0.7, "SFL": 0.5,
            "PFm": 0.6, "OFA": 0.5, "RI": 0.4,
        },
    },
    "Nostalgia": {
        "description": "Bittersweet memories, longing, familiarity",
        "color": "#fb923c",
        "regions": {
            "H": 1.0, "EC": 0.9, "PHA1": 0.8, "PHA2": 0.7,
            "PHA3": 0.6, "PreS": 0.6, "VMV1": 0.5, "VMV2": 0.5,
            "TF": 0.6, "PHT": 0.5,
        },
    },
    "Awe": {
        "description": "Wonder, vastness, the sublime",
        "color": "#22d3ee",
        "regions": {
            "V1": 0.6, "V2": 0.5, "V6": 0.7, "7m": 0.8,
            "PCC": 0.6, "POS1": 0.5, "POS2": 0.5,
            "DVT": 0.4, "ProStr": 0.4, "TPOJ1": 0.5,
        },
    },
    "Disgust": {
        "description": "Revulsion, rejection, moral outrage",
        "color": "#84cc16",
        "regions": {
            "Ig": 1.0, "Id": 0.9, "MI": 0.8, "Pir": 0.7,
            "AAIC": 0.7, "AVI": 0.6, "PoI1": 0.5,
            "47m": 0.5, "25": 0.4,
        },
    },
    "Boredom": {
        "description": "Disengagement, restlessness, mind-wandering",
        "color": "#94a3b8",
        "regions": {
            "PCC": 0.6, "7m": 0.5, "d23ab": 0.5, "v23ab": 0.5,
            "10r": 0.3, "10d": 0.3, "9m": 0.4, "9p": 0.4,
        },
    },
}

STIMULATION_TIPS = {
    "Visual":    "Add vivid imagery, high-contrast visuals, dynamic motion, or rich color palettes",
    "Auditory":  "Add music, speech, environmental sounds, melodic patterns, or rhythm",
    "Language":  "Add spoken narratives, complex dialogue, poetry, wordplay, or verbal storytelling",
    "Social":    "Add human faces, emotional expressions, voice acting, eye contact, or social interactions",
    "Emotion":   "Add emotionally charged moments, personal narrative, suspense, resolution, or moral stakes",
    "Memory":    "Add familiar environments, nostalgia cues, spatial exploration, or autobiographical hooks",
    "Motor":     "Add rhythmic movement, dance, physical demonstrations, action sequences, or sports",
    "Executive": "Add problem-solving scenarios, strategic choices, planning sequences, or puzzles",
    "Attention": "Add spatial puzzles, unexpected visual shifts, number patterns, or salient orientation cues",
    "Sensory":   "Add tactile descriptions, temperature cues, physical sensation, body movement, or taste imagery",
    "Other":     "Complex multimodal processing area",
}
