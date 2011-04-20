#!/usr/bin/env ruby

require 'mysql2'

client = Mysql2::Client.new(:host => 'localhost', :username => 'root', :password => 'ackptoo123')

query = false
build = ""
table = ""
ARGF.read.split("\n").each do |line|
  if line =~ /^###/
    query = true
    sql = line.gsub(/^###[ ]+(.*)/, '\1')
    /^(DELETE FROM|INSERT INTO|UPDATE) ([^ ]+)/.match(sql)
    rm = Regexp.last_match(2)
    table = rm unless rm == nil

    build+=sql + ' '
  else
    if query == true

      cols = client.query("SHOW COLUMNS FROM #{table}", :symbolize_keys => true )
      col_names = Array.new
      cols.each do |col|
        col_names << col[:Field]
      end
      build = build.gsub(/@(\d+)/) do |s|
        #n = s[1..s.size].to_i - 1
        n = s[1..-1].to_i - 1
        col_names[n]
      end

      puts build
      build = ""
      table = ""
    end
    query = false
  end
end
