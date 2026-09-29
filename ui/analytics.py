from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


GA_MEASUREMENT_ID = "G-DZD2EN5SFV"
PRODUCTION_URL = "https://peter-atef-eng.streamlit.app"


def initialize_analytics() -> None:
    # The script patches the parent window once and its listeners persist across
    # reruns, so re-creating the iframe on every interaction is wasted work.
    if st.session_state.get("_analytics_initialized"):
        return
    st.session_state["_analytics_initialized"] = True
    components.html(
        f"""
        <script>
        (function () {{
            try {{
                const measurementId = "{GA_MEASUREMENT_ID}";
                const productionUrl = "{PRODUCTION_URL}";
                const parentWindow = window.parent;
                const parentDocument = parentWindow.document;

                if (!parentWindow || !parentDocument) {{
                    return;
                }}

                const pageState = parentWindow.__portfolioAnalytics || {{}};
                parentWindow.__portfolioAnalytics = pageState;

                function pagePath() {{
                    const location = parentWindow.location;
                    return location.pathname || "/";
                }}

                function pageLocation() {{
                    const location = parentWindow.location;
                    return location.origin + pagePath();
                }}

                function sourcePage() {{
                    return pagePath();
                }}

                if (!parentWindow.dataLayer) {{
                    parentWindow.dataLayer = [];
                }}

                if (!parentWindow.gtag) {{
                    parentWindow.gtag = function () {{
                        parentWindow.dataLayer.push(arguments);
                    }};
                }}

                const gtag = parentWindow.gtag;

                if (!parentDocument.getElementById("portfolio-ga4-script")) {{
                    const script = parentDocument.createElement("script");
                    script.id = "portfolio-ga4-script";
                    script.async = true;
                    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
                    script.onerror = function () {{}};
                    parentDocument.head.appendChild(script);
                }}

                if (!pageState.configured) {{
                    gtag("js", new Date());
                    gtag("config", measurementId, {{
                        send_page_view: false,
                        anonymize_ip: true,
                        allow_google_signals: false,
                        allow_ad_personalization_signals: false
                    }});
                    pageState.configured = true;
                    pageState.productionUrl = productionUrl;
                }}

                function trackPageViewIfChanged() {{
                    try {{
                        const path = pagePath();
                        if (pageState.lastPagePath === path) {{
                            return;
                        }}
                        pageState.lastPagePath = path;
                        gtag("event", "page_view", {{
                            page_location: pageLocation(),
                            page_path: path,
                            page_title: parentDocument.title
                        }});
                    }} catch (error) {{}}
                }}

                function safeEvent(name, parameters) {{
                    try {{
                        gtag("event", name, Object.assign({{
                            source_page: sourcePage()
                        }}, parameters || {{}}));
                    }} catch (error) {{}}
                }}

                function linkPath(anchor) {{
                    try {{
                        return new URL(anchor.getAttribute("href"), parentWindow.location.origin).pathname;
                    }} catch (error) {{
                        return "";
                    }}
                }}

                function handleClick(event) {{
                    try {{
                        const target = event.target.closest("a, button");
                        if (!target) {{
                            return;
                        }}

                        const href = target.getAttribute("href") || "";
                        const text = (target.innerText || target.textContent || "").trim().toLowerCase();
                        const path = target.tagName.toLowerCase() === "a" ? linkPath(target) : "";

                        if (href.indexOf("mail.google.com/mail/") !== -1 || text === "email" || text === "send email") {{
                            safeEvent("email_click", {{ link_type: "email" }});
                            return;
                        }}

                        if (href.indexOf("github.com") !== -1 || text.indexOf("github") !== -1) {{
                            safeEvent("github_click", {{ link_type: "github" }});
                            return;
                        }}

                        if (href.indexOf("linkedin.com") !== -1 || text.indexOf("linkedin") !== -1) {{
                            safeEvent("linkedin_click", {{ link_type: "linkedin" }});
                            return;
                        }}

                        if (text.indexOf("download resume") !== -1) {{
                            safeEvent("resume_download", {{ link_type: "resume" }});
                            return;
                        }}

                        if (path === "/market_dashboard") {{
                            safeEvent("market_dashboard_open", {{ link_type: "internal" }});
                            return;
                        }}

                        if (path === "/data_pipeline") {{
                            safeEvent("data_pipeline_open", {{ link_type: "internal" }});
                        }}
                    }} catch (error) {{}}
                }}

                if (!pageState.clickListenerAttached) {{
                    parentDocument.addEventListener("click", handleClick, true);
                    pageState.clickListenerAttached = true;
                }}

                if (!pageState.historyPatched) {{
                    ["pushState", "replaceState"].forEach(function (methodName) {{
                        const original = parentWindow.history[methodName];
                        parentWindow.history[methodName] = function () {{
                            const result = original.apply(this, arguments);
                            setTimeout(trackPageViewIfChanged, 0);
                            return result;
                        }};
                    }});
                    parentWindow.addEventListener("popstate", function () {{
                        setTimeout(trackPageViewIfChanged, 0);
                    }});
                    pageState.historyPatched = true;
                }}

                trackPageViewIfChanged();
            }} catch (error) {{}}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
