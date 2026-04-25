

export default function AboutPage() {
    return (
        <div className="page-content about-page">
            <h1 className="section-title">About the <span className="neon-text">VC-UY1 Project</span></h1>

            <section className="research-context glass">
                <h2>Bridging the Digital Divide</h2>
                <p>
                    Volunteer Computing (VC) provides a unique opportunity to harness underutilized compute resources.
                    However, in environments like ours (West Africa / Cameroon), resource availability is highly
                    impacted by **unstable electricity** and specific local usage patterns.
                </p>
                <p>
                    Our research focuses on creating **frugal, TinyML-based prediction models** that anticipate
                    machine availability while respecting the strict resource constraints of the host systems.
                </p>
            </section>

            <section className="key-pillars">
                <div className="pillar glass">
                    <h3>Frugality</h3>
                    <p>Models optimized to run with &lt; 10 MB RAM and minimal CPU impact.</p>
                </div>
                <div className="pillar glass">
                    <h3>Local Context</h3>
                    <p>First dataset of its kind modeling African power grid instability as a signal.</p>
                </div>
                <div className="pillar glass">
                    <h3>Empowerment</h3>
                    <p>Turning every laptop into a node for high-performance scientific research.</p>
                </div>
            </section>
        </div>
    );
}
