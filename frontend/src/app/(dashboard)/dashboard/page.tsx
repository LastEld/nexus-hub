export default function DashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <p className="text-muted-foreground mt-2">
                    Welcome to NexusHub - Your Business Management Platform
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-lg border bg-card p-6">
                    <div className="text-2xl font-bold">107+</div>
                    <p className="text-xs text-muted-foreground">API Endpoints</p>
                </div>
                <div className="rounded-lg border bg-card p-6">
                    <div className="text-2xl font-bold">5</div>
                    <p className="text-xs text-muted-foreground">Domains</p>
                </div>
                <div className="rounded-lg border bg-card p-6">
                    <div className="text-2xl font-bold">12</div>
                    <p className="text-xs text-muted-foreground">Database Tables</p>
                </div>
                <div className="rounded-lg border bg-card p-6">
                    <div className="text-2xl font-bold">Ready</div>
                    <p className="text-xs text-muted-foreground">Production Status</p>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-lg border bg-card p-6">
                    <h3 className="font-semibold mb-4">Quick Actions</h3>
                    <div className="space-y-2">
                        <a href="/crm/companies" className="block text-sm text-primary hover:underline">
                            → View Companies
                        </a>
                        <a href="/crm/contacts" className="block text-sm text-primary hover:underline">
                            → View Contacts
                        </a>
                        <a href="/crm/deals" className="block text-sm text-primary hover:underline">
                            → View Deals
                        </a>
                        <a href="/projects" className="block text-sm text-primary hover:underline">
                            → View Projects
                        </a>
                    </div>
                </div>

                <div className="rounded-lg border bg-card p-6">
                    <h3 className="font-semibold mb-4">System Status</h3>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span className="text-muted-foreground">Backend API</span>
                            <span className="text-green-600">● Online</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-muted-foreground">Database</span>
                            <span className="text-green-600">● Connected</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-muted-foreground">Cache</span>
                            <span className="text-green-600">● Active</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
