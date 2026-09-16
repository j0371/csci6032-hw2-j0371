# Agent Workflow Audit and Logging Policy

    Record agentic workflows. For every request that
    modifies the workspace—including creating, editing, moving, renaming, or deleting
    files—create a new Jupyter Notebook (`.ipynb`) under `/Workflows/` with a concise,
    descriptive name for the workflow. Treat this notebook as part of the requested
    work and complete it before declaring the task finished.

    The workflow notebook must provide a complete, chronological audit trail of the
    work performed. Include the user's request, the plan and any changes to that plan,
    files inspected or modified, commands run and their observed output, edits made,
    validation or tests performed and their results, errors or unexpected behavior,
    and the final response provided to the user. Also include any intermediate plans,
    TODOs, notes, temporary text, or other planning artifacts created during the
    workflow, along with concise summaries of reasoning or decisions that materially
    affected the work.

    Use the formatting and organizational features available in Jupyter notebooks to
    make the record as clear and readable as practical. Use Markdown cells, headings,
    subheadings, tables, lists, blockquotes, code blocks, horizontal sections, and
    other appropriate formatting to clearly distinguish stages of the workflow.
    Commands, source snippets, diffs, test output, errors, and other terminal output
    should be presented in clearly labeled code blocks or cells.

    As a general organizational pattern, structure the notebook around sections such
    as **Request**, **Initial Plan**, **Pre-change State**, **Work Log**, **Changes**,
    **Validation**, **Final State**, and **User Response**. These section names are
    guidance rather than a rigid required schema: omit sections that are not relevant,
    rename them when a clearer heading would better describe the work, and add
    additional sections where useful. Preserve a clear chronological progression so
    that a reader can reconstruct what the agent did, why it did it, and what result
    was observed.

    The notebook is an audit record, not the execution environment for the workflow.
    Do not rerun commands merely to reproduce them inside the notebook. Record the
    commands actually executed and the output actually observed during the workflow.
    Do not fabricate notebook outputs, execution results, or other evidence that was
    not actually observed.

    Do not omit failed attempts, intermediate results, or deviations from the
    original plan. The workflow record must accurately distinguish actions actually
    performed and results actually observed from proposed, inferred, or unverified
    actions. Do not include secrets, credentials, private data, or other information
    prohibited by this policy.

    Do not recursively audit the auditing process itself. Creating, updating,
    inspecting, formatting, or validating the workflow notebook required by this rule
    does not constitute a separate agentic workflow and must not trigger creation of
    another workflow record. Actions performed solely to maintain the current workflow
    notebook must never cause recursive logging, nested workflow records, or an audit
    loop.