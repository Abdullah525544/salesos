"use client";

import { BarChart3, Phone, Search, Target, Users } from "lucide-react";
import { FormEvent, useEffect, useRef, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useAuth } from "@/lib/auth";

type SalesLead = {
  id: number;
  business_name: string;
  phone_number: string | null;
  email: string | null;
  website: string | null;
  city: string | null;
  country: string | null;
  niche: string | null;
  pipeline_stage: string;
  qualification_score: number | null;
  classification: string | null;
  research_status: string;
};

type LeadsResponse = {
  leads: SalesLead[];
  total: number;
};

type Analytics = {
  total_leads: number;
  calls_made: number;
  connected_calls: number;
  interested_leads: number;
  meetings_booked: number;
  conversion_rate: number;
  revenue_generated: number;
  hot_leads: number;
  warm_leads: number;
  cold_leads: number;
};

const emptyAnalytics: Analytics = {
  total_leads: 0,
  calls_made: 0,
  connected_calls: 0,
  interested_leads: 0,
  meetings_booked: 0,
  conversion_rate: 0,
  revenue_generated: 0,
  hot_leads: 0,
  warm_leads: 0,
  cold_leads: 0,
};

export default function SalesOSPage() {
  const { user, getAccessToken, redirectToLogin, loading } = useAuth();
  const [leads, setLeads] = useState<SalesLead[]>([]);
  const [analytics, setAnalytics] = useState<Analytics>(emptyAnalytics);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [form, setForm] = useState({
    niche: "",
    country: "",
    city: "",
    keyword: "",
    category: "",
  });
  const hasFetched = useRef(false);

  useEffect(() => {
    if (!loading && !user) {
      redirectToLogin();
    }
  }, [loading, user, redirectToLogin]);

  const authedFetch = async <T,>(path: string, init?: RequestInit): Promise<T> => {
    const token = await getAccessToken();
    const response = await fetch(`/api/v1/sales-os${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(init?.headers ?? {}),
      },
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return response.json();
  };

  const refresh = async () => {
    setIsLoading(true);
    try {
      const [leadData, analyticsData] = await Promise.all([
        authedFetch<LeadsResponse>("/leads?limit=100"),
        authedFetch<Analytics>("/analytics"),
      ]);
      setLeads(leadData.leads);
      setAnalytics(analyticsData);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (loading || !user || hasFetched.current) {
      return;
    }
    hasFetched.current = true;
    refresh().catch((error) => console.error("Failed to load Sales OS", error));
  }, [loading, user]);

  const submitLeadSearch = async (event: FormEvent) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await authedFetch<LeadsResponse>("/lead-finder/search", {
        method: "POST",
        body: JSON.stringify({
          niche: form.niche,
          country: form.country || null,
          city: form.city || null,
          keyword: form.keyword || null,
          category: form.category || null,
          limit: 50,
        }),
      });
      await refresh();
    } finally {
      setIsSubmitting(false);
    }
  };

  const createManualLead = async () => {
    if (!form.niche.trim()) {
      return;
    }
    setIsSubmitting(true);
    try {
      await authedFetch<SalesLead>("/leads", {
        method: "POST",
        body: JSON.stringify({
          business_name: form.keyword || `${form.niche} lead`,
          niche: form.niche,
          country: form.country || null,
          city: form.city || null,
          category: form.category || null,
          lead_source: "manual",
        }),
      });
      await refresh();
    } finally {
      setIsSubmitting(false);
    }
  };

  const metricCards = [
    { label: "Total Leads", value: analytics.total_leads, icon: Users },
    { label: "Calls Made", value: analytics.calls_made, icon: Phone },
    { label: "Interested", value: analytics.interested_leads, icon: Target },
    { label: "Conversion", value: `${analytics.conversion_rate}%`, icon: BarChart3 },
  ];

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold">Sales OS</h1>
        <p className="text-muted-foreground">
          Lead finder, prospect research, CRM pipeline, call intelligence, and sales analytics.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        {metricCards.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.label}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{metric.label}</CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metric.value}</div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Lead Finder
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form className="grid gap-3 md:grid-cols-6" onSubmit={submitLeadSearch}>
            <Input
              placeholder="Niche"
              value={form.niche}
              onChange={(event) => setForm({ ...form, niche: event.target.value })}
              required
            />
            <Input
              placeholder="Country"
              value={form.country}
              onChange={(event) => setForm({ ...form, country: event.target.value })}
            />
            <Input
              placeholder="City"
              value={form.city}
              onChange={(event) => setForm({ ...form, city: event.target.value })}
            />
            <Input
              placeholder="Keyword"
              value={form.keyword}
              onChange={(event) => setForm({ ...form, keyword: event.target.value })}
            />
            <Input
              placeholder="Category"
              value={form.category}
              onChange={(event) => setForm({ ...form, category: event.target.value })}
            />
            <div className="flex gap-2">
              <Button type="submit" disabled={isSubmitting}>
                Search
              </Button>
              <Button type="button" variant="outline" disabled={isSubmitting} onClick={createManualLead}>
                Add
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>CRM Pipeline</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, index) => (
                <div key={index} className="h-12 animate-pulse rounded bg-muted" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Business</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Contact</TableHead>
                  <TableHead>Stage</TableHead>
                  <TableHead>Research</TableHead>
                  <TableHead>Score</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {leads.map((lead) => (
                  <TableRow key={lead.id}>
                    <TableCell>
                      <div className="font-medium">{lead.business_name}</div>
                      <div className="text-sm text-muted-foreground">{lead.niche || lead.website}</div>
                    </TableCell>
                    <TableCell>{[lead.city, lead.country].filter(Boolean).join(", ") || "-"}</TableCell>
                    <TableCell>
                      <div>{lead.phone_number || "-"}</div>
                      <div className="text-sm text-muted-foreground">{lead.email || ""}</div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{lead.pipeline_stage.replaceAll("_", " ")}</Badge>
                    </TableCell>
                    <TableCell>{lead.research_status}</TableCell>
                    <TableCell>
                      {lead.qualification_score ?? "-"}
                      {lead.classification ? ` ${lead.classification}` : ""}
                    </TableCell>
                  </TableRow>
                ))}
                {!leads.length && (
                  <TableRow>
                    <TableCell colSpan={6} className="py-8 text-center text-muted-foreground">
                      No leads yet.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
