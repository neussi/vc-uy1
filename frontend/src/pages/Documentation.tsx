

export default function DocumentationPage() {
    return (
        <div className="page-content doc-page">
            <h1 className="section-title">Technical <span className="neon-text">Documentation</span></h1>

            <div className="doc-grid">
                <aside className="doc-sidebar glass">
                    <ul>
                        <li><a href="#overview">System Overview</a></li>
                        <li><a href="#agent">The VC Agent</a></li>
                        <li><a href="#data">Data Collection</a></li>
                        <li><a href="#security">Security & Privacy</a></li>
                    </ul>
                </aside>

                <section className="doc-main glass">
                    <h2 id="overview">System Overview</h2>
                    <p>
                        The VC-UY1 system uses a two-tier architecture (Global Model / Local Model)
                        to predict availability. The system is designed to be low-latency and high-accuracy.
                    </p>

                    <h2 id="agent">The VC Agent</h2>
                    <p>
                        The agent is a background service written in Python. It cycles every 5 minutes to
                        collect resource snapshots. It includes:
                    </p>
                    <ul>
                        <li><strong>Collector</strong>: Hardware monitoring.</li>
                        <li><strong>Heartbeat</strong>: Power-cut detection logic.</li>
                        <li><strong>Syncer</strong>: Batch data transmission to the central server.</li>
                    </ul>

                    <h2 id="data">Data Collection Parameters</h2>
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Field</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>CPU %</td>
                                    <td>Current CPU utilization.</td>
                                </tr>
                                <tr>
                                    <td>RAM %</td>
                                    <td>Memory footprint of the system.</td>
                                </tr>
                                <tr>
                                    <td>Power Cut Flag</td>
                                    <td>Binary marker if the previous session ended abruptly.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>
            </div>
        </div>
    );
}
